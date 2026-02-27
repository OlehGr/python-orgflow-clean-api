import enum
import uuid
from datetime import datetime
from typing import TypeVar

import msgspec

from app.core.models.base import IdDto, get_native_utc_now


class EntityEventSubject(enum.StrEnum):
    user_register = "user_register"


class EntityEventEntity(enum.StrEnum):
    user = "user"


TEntity = TypeVar("TEntity", bound=IdDto, default=IdDto)


class EntityEvent[TEntity](msgspec.Struct, frozen=True):
    producer_id: uuid.UUID | None
    subject: EntityEventSubject
    entity: EntityEventEntity
    entity_id: uuid.UUID
    data: TEntity
    space_id: uuid.UUID | None = None
    id: uuid.UUID = msgspec.field(default_factory=uuid.uuid4)
    created_at: datetime = msgspec.field(default_factory=get_native_utc_now)
