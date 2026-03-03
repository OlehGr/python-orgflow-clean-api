import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import EntityDto, EntityModel, get_native_utc_now


class FileModel(EntityModel):
    __tablename__ = "file"

    url: Mapped[str]
    name: Mapped[str]
    size: Mapped[int]
    content_type: Mapped[str]

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)

    @classmethod
    def create(
        cls,
        *,
        file_id: uuid.UUID,
        url: str,
        name: str,
        size: int,
        content_type: str,
        author_id: uuid.UUID,
    ) -> "FileModel":
        return cls(
            is_removed=False,
            created_at=get_native_utc_now(),
            updated_at=get_native_utc_now(),
            id=file_id,
            url=url,
            name=name,
            size=size,
            content_type=content_type,
            author_id=author_id,
        )

    async def set_file_source(self, *, url: str, size: int) -> None:
        self.url = url
        self.size = size


class FileEventDto(EntityDto, frozen=True):
    url: str
    name: str
    size: int
    content_type: str
    author_id: uuid.UUID

    @classmethod
    def from_file(cls, file: FileModel) -> "FileEventDto":
        return cls(
            id=file.id,
            created_at=file.created_at,
            updated_at=file.updated_at,
            is_removed=file.is_removed,
            url=file.url,
            size=file.size,
            content_type=file.content_type,
            name=file.name,
            author_id=file.author_id,
        )
