import uuid
from datetime import datetime
from typing import TypedDict

from sqlalchemy.orm import Mapped, mapped_column, reconstructor

from app.core.models.entity_event import EntityEvent
from .base import IdDto, IdModel, get_native_utc_now


class EntityBaseArgs(TypedDict):
    id: uuid.UUID
    is_removed: bool
    created_at: datetime
    updated_at: datetime


class EntityModel(IdModel):
    __abstract__ = True

    is_removed: Mapped[bool] = mapped_column(index=True)

    created_at: Mapped[datetime] = mapped_column(index=True)
    updated_at: Mapped[datetime] = mapped_column(index=True, onupdate=get_native_utc_now)

    _events: list[EntityEvent]

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self._init_internal_state()

    @reconstructor
    def _sa_init_on_load(self) -> None:
        self._init_internal_state()

    def _init_internal_state(self) -> None:
        self._events = []

    def add_events(self, *events: EntityEvent) -> None:
        self._events.extend(events)

    def pop_events(self) -> list[EntityEvent]:
        events = self._events
        self._events = []
        return events

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
