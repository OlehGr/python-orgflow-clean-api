from abc import abstractmethod
from typing import Protocol

from app.core.models import EntityEventModel


class IEntityEventRepository(Protocol):
    @abstractmethod
    async def save(self, event: EntityEventModel) -> None: ...
