import uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field

from app.core.models import FileModel
from app.core.models.base import EntityDto


class FileReadDto(EntityDto, frozen=True):
    url: str
    name: str
    size: int
    content_type: str

    @classmethod
    def from_file(cls, file: FileModel) -> "FileReadDto":
        return cls(
            id=file.id,
            created_at=file.created_at,
            updated_at=file.updated_at,
            is_removed=file.is_removed,
            url=file.url,
            size=file.size,
            content_type=file.content_type,
            name=file.name,
        )


@dataclass(frozen=True)
class FileCreateStreamData:
    name: str
    content_type: str
    file_stream: AsyncGenerator[bytes]


@dataclass(frozen=True)
class FileUploadStreamData:
    file_id: uuid.UUID
    file_stream: AsyncGenerator[bytes]
    file_name: str
    content_type: str
    file_name_prefix: str | None = field(default=None)


@dataclass(frozen=True)
class FileUploadData:
    file_id: uuid.UUID
    file_data: bytes
    file_name: str
    content_type: str
    file_name_prefix: str | None = field(default=None)


@dataclass(frozen=True)
class FileUploadResult:
    file_url: str
    file_size: int


@dataclass(frozen=True)
class ImagerCompressResult:
    optimized_data: bytes
    content_type: str
    file_name: str
