import uuid
from dataclasses import dataclass

from app.core.application.dto.file import FileCreateStreamData, FileUploadStreamData
from app.core.application.interfaces.repository.file import IFileRepository
from app.core.application.interfaces.services.file import IFileStorage
from app.core.models import FileModel


@dataclass
class FileService:
    _file_storage: IFileStorage

    _file_repository: IFileRepository

    async def create_file_from_stream(self, data: FileCreateStreamData, *, actor_id: uuid.UUID) -> uuid.UUID:
        file_id = uuid.uuid4()
        result = await self._file_storage.upload_file_stream(
            FileUploadStreamData(
                file_id=file_id,
                file_name=data.name,
                content_type=data.content_type,
                file_stream=data.file_stream,
            )
        )

        file = FileModel.create(
            file_id=file_id,
            url=result.file_url,
            name=data.name,
            size=result.file_size,
            content_type=data.content_type,
            author_id=actor_id,
        )

        await self._file_repository.save(file, actor_id=actor_id)

        return file.id
