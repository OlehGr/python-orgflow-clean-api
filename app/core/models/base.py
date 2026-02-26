import uuid
from datetime import UTC, datetime
from typing import Any

import msgspec
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry


mapper_registry = registry(metadata=MetaData())


class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __abstract__ = True


class IdModel(BaseModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, unique=True, default=uuid.uuid4)


class EntityModel(IdModel):
    __abstract__ = True

    is_removed: Mapped[bool] = mapped_column(index=True)

    created_at: Mapped[datetime] = mapped_column(index=True)
    updated_at: Mapped[datetime] = mapped_column(index=True, onupdate="get_native_utc_now")

    @classmethod
    def _generate_base_args(cls) -> dict[str, Any]:
        return {
            "id": uuid.uuid4(),
            "is_removed": False,
            "created_at": get_native_utc_now(),
            "updated_at": get_native_utc_now(),
        }


def get_native_utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class IdDto(msgspec.Struct, frozen=True):
    id: uuid.UUID


class EntityDto(IdDto, frozen=True):
    is_removed: bool
    created_at: datetime
    updated_at: datetime
