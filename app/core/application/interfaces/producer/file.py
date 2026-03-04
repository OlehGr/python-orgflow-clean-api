import uuid
from abc import abstractmethod
from typing import Protocol


class IFileCompressProducer(Protocol):
    @abstractmethod
    async def send(self, file_id: uuid.UUID) -> None: ...
