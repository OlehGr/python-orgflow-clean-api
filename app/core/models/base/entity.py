import uuid
from datetime import datetime
from typing import TypedDict, TypeVar

from sqlalchemy.orm import Mapped, mapped_column

from .base import IdDto, IdModel
from .helpers import get_native_utc_now


class EntityBaseArgs(TypedDict):
    id: uuid.UUID
    is_removed: bool
    created_at: datetime
    updated_at: datetime


TCreateSubject = TypeVar("TCreateSubject", bound=str)
TUpdateSubject = TypeVar("TUpdateSubject", bound=str)


class EntityModel(IdModel):
    __abstract__ = True

    is_removed: Mapped[bool] = mapped_column(index=True)

    created_at: Mapped[datetime] = mapped_column(index=True)
    updated_at: Mapped[datetime] = mapped_column(index=True, onupdate=get_native_utc_now)

    __is_created: bool = False

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.__is_created = True

    def _resolve_entity_save_subject(
        self, create_subject: TCreateSubject, update_subject: TUpdateSubject
    ) -> TCreateSubject | TUpdateSubject:
        if self.__is_created:
            self.__is_created = False
            return create_subject

        return update_subject

    @classmethod
    def _generate_base_args(cls) -> EntityBaseArgs:
        return {
            "id": uuid.uuid4(),
            "is_removed": False,
            "created_at": get_native_utc_now(),
            "updated_at": get_native_utc_now(),
        }


class EntityDto(IdDto, frozen=True):
    is_removed: bool
    created_at: datetime
    updated_at: datetime
