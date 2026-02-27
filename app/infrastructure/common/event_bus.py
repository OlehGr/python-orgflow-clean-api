from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Literal

from app.core.application.interfaces.common.background import IBackgroundExecutor
from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.models.event import EntityEvent, EntityEventSubject


AllSubjects = Literal["ALL_SUBJECTS"]


@dataclass
class InMemoryEventBus(IEntityEventBus):
    _handlers: dict[EntityEventSubject | AllSubjects, list[Callable[[EntityEvent], Coroutine]]]
    _background_executor: IBackgroundExecutor

    def __init__(self, background_executor: IBackgroundExecutor) -> None:
        self._handlers = {"ALL_SUBJECTS": []}
        self._background_executor = background_executor

    def publish(self, event: EntityEvent) -> None:
        for handler in self._handlers["ALL_SUBJECTS"]:
            self._background_executor.submit(handler(event))

        if event.subject not in self._handlers:
            return

        for handler in self._handlers[event.subject]:
            self._background_executor.submit(handler(event))

    def subscribe(
        self,
        subjects: set[EntityEventSubject] | None,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None:
        if not subjects:
            self._handlers["ALL_SUBJECTS"].append(handler)
            return

        for subject in subjects:
            if subject not in self._handlers:
                self._handlers[subject] = []
            self._handlers[subject].append(handler)

    def unsubscribe(
        self,
        subjects: set[EntityEventSubject] | None,
        handler: Callable[[EntityEvent], Coroutine],
    ) -> None:
        if not subjects:
            handlers = self._handlers.get("ALL_SUBJECTS")
            if handlers:
                handlers.remove(handler)
            return

        for subject in subjects:
            handlers = self._handlers.get(subject)
            if handlers:
                handlers.remove(handler)
