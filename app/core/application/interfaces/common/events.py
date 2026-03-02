from abc import abstractmethod
from collections.abc import Callable, Coroutine
from typing import Protocol

from app.core.models.entity_event import EntityEvent, EntityEventAllSubjects, EntityEventSubject


class IEntityEventBus(Protocol):
    @abstractmethod
    async def publish(self, event: EntityEvent) -> None: ...

    @abstractmethod
    def subscribe(
        self,
        subjects: set[EntityEventSubject] | EntityEventAllSubjects,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None: ...

    @abstractmethod
    def unsubscribe(
        self,
        subjects: set[EntityEventSubject] | EntityEventAllSubjects,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None: ...
