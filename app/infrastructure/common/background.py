import asyncio
from typing import TYPE_CHECKING

from app.core.application.interfaces.common.background import IBackgroundExecutor


if TYPE_CHECKING:
    from collections.abc import Coroutine


class BackgroundExecutor(IBackgroundExecutor):
    _tasks: set[asyncio.Task]

    def __init__(self) -> None:
        self._tasks = set()

    def submit(self, coroutine: Coroutine) -> None:
        loop = asyncio.get_event_loop()
        task = loop.create_task(coroutine)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
