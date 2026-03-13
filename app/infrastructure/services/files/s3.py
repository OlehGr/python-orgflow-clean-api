import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from aiobotocore.session import AioSession, get_session

from app.core.application.dto.file import FileUploadData, FileUploadResult, FileUploadStreamData
from app.core.application.interfaces.services.file import IFileStorage
from app.core.config import env_config
from app.core.exceptions.validation import ConflictError
from app.core.models import FileModel


if TYPE_CHECKING:
    from types_aiobotocore_s3.client import S3Client
    from types_aiobotocore_s3.type_defs import CompletedPartTypeDef


class S3FileStorage(IFileStorage):
    session: AioSession

    def __init__(self) -> None:
        self.session = get_session()

    async def upload_file_data(self, data: FileUploadData) -> FileUploadResult:
        object_key = self._generate_object_key(
            file_id=data.file_id, file_name=data.file_name, file_name_prefix=data.file_name_prefix
        )
        bucket = env_config.s3_bucket

        async with self._get_client() as client:
            await client.put_object(
                Bucket=bucket,
                Key=object_key,
                Body=data.file_data,
                ACL="public-read",
                ContentType=data.content_type,
            )

            head = await client.head_object(Bucket=bucket, Key=object_key)
            file_size = head["ContentLength"]

            file_url = self._generate_file_url(object_key)
            return FileUploadResult(file_url=file_url, file_size=file_size)

    async def upload_file_stream(self, data: FileUploadStreamData) -> FileUploadResult:
        object_key = self._generate_object_key(
            file_id=data.file_id, file_name=data.file_name, file_name_prefix=data.file_name_prefix
        )
        bucket = env_config.s3_bucket

        async with self._get_client() as client:
            multipart = await client.create_multipart_upload(
                Bucket=bucket,
                Key=object_key,
                ACL="public-read",
                ContentType=data.content_type,
            )
            upload_id = multipart["UploadId"]
            parts: list[CompletedPartTypeDef] = []
            total = 0
            part_number = 1
            current_chunk = bytearray()

            try:
                async for chunk in data.file_stream:
                    total += len(chunk)

                    self._validate_size(total)

                    current_chunk.extend(chunk)

                    if len(current_chunk) >= 5 * 1024 * 1024:
                        resp = await client.upload_part(
                            Bucket=bucket,
                            Key=object_key,
                            PartNumber=part_number,
                            UploadId=upload_id,
                            Body=bytes(current_chunk),
                        )
                        parts.append({"PartNumber": part_number, "ETag": resp["ETag"]})
                        part_number += 1
                        current_chunk.clear()

                if current_chunk:
                    resp = await client.upload_part(
                        Bucket=bucket,
                        Key=object_key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=bytes(current_chunk),
                    )
                    parts.append({"PartNumber": part_number, "ETag": resp["ETag"]})

                await client.complete_multipart_upload(
                    Bucket=bucket,
                    Key=object_key,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts},
                )

            except Exception as e:
                await client.abort_multipart_upload(Bucket=bucket, Key=object_key, UploadId=upload_id)
                raise ConflictError("Ошибка загрузки файла") from e

            head = await client.head_object(Bucket=bucket, Key=object_key)
            file_size = head["ContentLength"]

            file_url = self._generate_file_url(object_key)
            return FileUploadResult(file_url=file_url, file_size=file_size)

    async def get_uploaded_file(self, file: FileModel) -> bytes:
        object_key = file.file_url_key
        bucket = env_config.s3_bucket

        async with self._get_client() as s3:
            obj = await s3.get_object(Bucket=bucket, Key=object_key)
            return await obj["Body"].read()

    def _generate_object_key(self, *, file_id: uuid.UUID, file_name: str, file_name_prefix: str | None) -> str:
        end = f"{file_name_prefix}/{file_name}" if file_name_prefix else file_name
        return f"{env_config.s3_directory}/{env_config.s3_prefix}/{file_id}/{end}"

    def _generate_file_url(self, object_key: str) -> str:
        return f"{env_config.s3_public_url or env_config.s3_url}/{env_config.s3_bucket}/{object_key}"

    def _validate_size(self, size: int) -> None:
        max_bytes = 1024 * 1024 * 1024

        if size > max_bytes:
            raise ConflictError("Файл слишком большой")

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator["S3Client"]:
        async with self.session.create_client(
            "s3",
            aws_access_key_id=env_config.s3_access_key,
            aws_secret_access_key=env_config.s3_secret_key,
            endpoint_url=env_config.s3_url,
        ) as client:
            yield client
