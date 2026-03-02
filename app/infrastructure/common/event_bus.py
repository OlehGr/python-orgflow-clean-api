from collections.abc import Callable, Coroutine
from dataclasses import dataclass

from app.core.application.interfaces.common.background import IBackgroundExecutor
from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.models.entity_event import EntityEvent, EntityEventAllSubjects, EntityEventSubject


@dataclass
class InMemoryEntityEventBus(IEntityEventBus):
    _handlers: dict[EntityEventSubject | EntityEventAllSubjects, list[Callable[[EntityEvent], Coroutine]]]
    _background_executor: IBackgroundExecutor

    def __init__(self, background_executor: IBackgroundExecutor) -> None:
        self._handlers = {"*": []}
        self._background_executor = background_executor

    async def publish(self, event: EntityEvent) -> None:
        for handler in self._handlers["*"]:
            self._background_executor.submit(handler(event))

        if event.subject not in self._handlers:
            return

        for handler in self._handlers[event.subject]:
            self._background_executor.submit(handler(event))

    def subscribe(
        self,
        subjects: set[EntityEventSubject] | EntityEventAllSubjects,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None:
        if isinstance(subjects, str):
            self._handlers[subjects].append(handler)
            return

        for subject in subjects:
            if subject not in self._handlers:
                self._handlers[subject] = []
            self._handlers[subject].append(handler)

    def unsubscribe(
        self,
        subjects: set[EntityEventSubject] | EntityEventAllSubjects,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None:
        if isinstance(subjects, str):
            handlers = self._handlers.get(subjects)
            if handlers:
                handlers.remove(handler)
            return

        for subject in subjects:
            handlers = self._handlers.get(subject)
            if handlers:
                handlers.remove(handler)
