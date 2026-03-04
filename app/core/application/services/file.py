import uuid
from dataclasses import dataclass

from app.core.application.dto.file import FileCreateStreamData, FileUploadData, FileUploadStreamData
from app.core.application.interfaces.managers.transaction import ITransactionManager
from app.core.application.interfaces.producer.file import IFileCompressProducer
from app.core.application.interfaces.repository.file import IFileRepository
from app.core.application.interfaces.services.file import IFileStorage, IImageCompressor, IImageHasher
from app.core.models import FileModel


@dataclass
class FileService:
    _tm: ITransactionManager
    _file_storage: IFileStorage
    _file_repository: IFileRepository
    _file_compress_producer: IFileCompressProducer

    async def create_file_from_stream(self, data: FileCreateStreamData, *, actor_id: uuid.UUID) -> uuid.UUID:
        file_id = uuid.uuid4()
        file_name = FileModel.normalize_file_name(data.name)

        result = await self._file_storage.upload_file_stream(
            FileUploadStreamData(
                file_id=file_id,
                file_name=file_name,
                content_type=data.content_type,
                file_stream=data.file_stream,
            )
        )

        file = FileModel.create(
            file_id=file_id,
            url=result.file_url,
            name=file_name,
            size=result.file_size,
            content_type=data.content_type,
            author_id=actor_id,
        )

        async with self._tm.transaction():
            await self._file_repository.save(file, actor_id=actor_id)
            await self._file_compress_producer.send(file.id)

        return file.id


@dataclass
class FileOptimizeService:
    _image_optimizer: IImageCompressor
    _image_hasher: IImageHasher
    _file_storage: IFileStorage

    _file_repository: IFileRepository

    async def compress_file(self, file_id: uuid.UUID) -> None:
        file = await self._file_repository.get_by_id(file_id)

        if not file.is_image:
            return

        image_data = await self._file_storage.get_uploaded_file(file)

        image_compress_result = await self._image_optimizer.compress_image(image_data=image_data, image_name=file.name)

        compressed_upload = await self._file_storage.upload_file_data(
            FileUploadData(
                file_id=file.id,
                file_data=image_compress_result.optimized_data,
                file_name=image_compress_result.file_name,
                content_type=image_compress_result.content_type,
            )
        )

        file.set_image_data(
            name=image_compress_result.file_name,
            content_type=image_compress_result.content_type,
            url=compressed_upload.file_url,
            size=compressed_upload.file_size,
        )

        image_hash = await self._image_hasher.hash_image(image_compress_result.optimized_data)

        file.set_file_hash(image_hash)

        await self._file_repository.save(file, actor_id=None)
