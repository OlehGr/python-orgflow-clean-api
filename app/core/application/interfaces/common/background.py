from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from collections.abc import Coroutine


class IBackgroundExecutor(Protocol):
    @abstractmethod
    def submit(self, coroutine: Coroutine) -> None: ...
