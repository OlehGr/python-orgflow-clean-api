import uuid
from abc import abstractmethod
from typing import Protocol

from app.core.models.file import FileModel


class IFileRepository(Protocol):
    @abstractmethod
    async def save(self, file: FileModel) -> None: ...

    @abstractmethod
    async def get_by_id(self, file_id: uuid.UUID) -> FileModel: ...
