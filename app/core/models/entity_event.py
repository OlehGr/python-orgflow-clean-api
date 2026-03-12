import enum
import uuid
from datetime import datetime
from typing import Any, Literal, TypeVar

import msgspec
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import IdDto, IdModel, get_native_utc_now


EntityEventAllSubjects = Literal["*"]


class EntityEventSubject(enum.StrEnum):
    user_create = "user_create"
    user_update = "user_update"
    user_delete = "user_delete"

    file_save = "file_save"
    file_delete = "file_delete"

    organization_save = "organization_save"
    organization_delete = "organization_delete"

    organization_member_save = "organization_member_save"
    organization_member_delete = "organization_member_delete"

    project_save = "project_save"
    project_delete = "project_delete"


class EntityEventEntity(enum.StrEnum):
    user = "user"
    file = "file"
    organization = "organization"
    organization_member = "organization_member"
    project = "project"


TEntity = TypeVar("TEntity", bound=IdDto, default=IdDto)


class EntityEvent[TEntity](msgspec.Struct, frozen=True):
    producer_id: uuid.UUID | None
    subject: EntityEventSubject
    entity: EntityEventEntity
    entity_id: uuid.UUID
    data: TEntity
    id: uuid.UUID = msgspec.field(default_factory=uuid.uuid4)
    created_at: datetime = msgspec.field(default_factory=get_native_utc_now)


class EntityEventModel(IdModel):
    __tablename__ = "entity_event"

    created_at: Mapped[datetime] = mapped_column(index=True)
    producer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"), nullable=True, index=True
    )
    entity: Mapped[EntityEventEntity] = mapped_column(String(), index=True)
    subject: Mapped[EntityEventSubject] = mapped_column(String())
    entity_id: Mapped[uuid.UUID] = mapped_column(index=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB())

    @classmethod
    def create(
        cls,
        *,
        event_id: uuid.UUID,
        subject: EntityEventSubject,
        entity_id: uuid.UUID,
        entity: EntityEventEntity,
        producer_id: uuid.UUID | None,
        data: dict[str, Any],
    ) -> "EntityEventModel":
        return cls(
            id=event_id,
            created_at=get_native_utc_now(),
            producer_id=producer_id,
            entity=entity,
            subject=subject,
            entity_id=entity_id,
            data=data,
        )
