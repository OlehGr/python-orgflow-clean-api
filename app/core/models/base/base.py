import uuid

import msgspec
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, registry


mapper_registry = registry(metadata=MetaData())


class BaseModel(MappedAsDataclass, DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __abstract__ = True


class IdModel(BaseModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)


class IdDto(msgspec.Struct, frozen=True):
    id: uuid.UUID
