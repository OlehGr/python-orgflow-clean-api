import uuid
from abc import abstractmethod
from typing import Protocol


class IImageOptimizeProducer(Protocol):
    @abstractmethod
    async def send(self, file_id: uuid.UUID) -> None: ...
