from abc import abstractmethod
from collections.abc import Callable, Coroutine
from typing import Protocol

from app.core.models.event import EntityEvent, EntityEventSubject


class IEntityEventBus(Protocol):
    @abstractmethod
    def publish(self, event: EntityEvent) -> None: ...

    @abstractmethod
    def subscribe(
        self,
        subjects: set[EntityEventSubject] | None,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None: ...

    @abstractmethod
    def unsubscribe(
        self,
        subjects: set[EntityEventSubject] | None,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None: ...
