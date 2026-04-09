import uuid
from urllib.parse import urlparse

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import get_native_utc_now
from app.core.models.entity import EntityDto, EntityModel
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject


class FileModel(EntityModel):
    __tablename__ = "file"

    url: Mapped[str]
    name: Mapped[str]
    size: Mapped[int]
    content_type: Mapped[str]
    hash: Mapped[str | None]

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
        actor_id: uuid.UUID,
        hash_: str | None = None,
    ) -> "FileModel":
        entity = cls(
            is_removed=False,
            created_at=get_native_utc_now(),
            updated_at=get_native_utc_now(),
            id=file_id,
            url=url,
            name=cls.normalize_file_name(name),
            size=size,
            content_type=content_type,
            author_id=actor_id,
            hash=hash_,
        )
        entity.add_events(entity.to_entity_subject_event(EntityEventSubject.file_create, actor_id=actor_id))
        return entity

    def set_file_hash(self, hash_: str, *, actor_id: uuid.UUID | None) -> None:
        self.hash = hash_
        self.add_events(self.to_entity_subject_event(EntityEventSubject.file_update, actor_id=actor_id))

    def set_image_data(
        self, *, name: str, content_type: str, url: str, size: int, actor_id: uuid.UUID | None
    ) -> None:
        self.name = name
        self.content_type = content_type
        self.url = url
        self.size = size
        self.add_events(self.to_entity_subject_event(EntityEventSubject.file_update, actor_id=actor_id))

    def delete(self, *, actor_id: uuid.UUID | None) -> None:
        self.add_events(self.to_entity_subject_event(EntityEventSubject.file_delete, actor_id=actor_id))

    @staticmethod
    def normalize_file_name(name: str) -> str:
        return name.lower()

    @property
    def is_image(self) -> bool:
        return self.content_type.lower().startswith("image/")

    @property
    def file_url_key(self) -> str:
        return urlparse(self.url).path.lstrip("/").split("/", 1)[1]

    def to_entity_subject_event(
        self, subject: EntityEventSubject, *, actor_id: uuid.UUID | None
    ) -> EntityEvent["FileEventDto"]:
        return EntityEvent(
            producer_id=actor_id,
            subject=subject,
            entity=EntityEventEntity.file,
            entity_id=self.id,
            data=FileEventDto.from_file(self),
        )


class FileEventDto(EntityDto, frozen=True):
    url: str
    name: str
    size: int
    content_type: str
    hash: str | None
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
            hash=file.hash,
            author_id=file.author_id,
        )
