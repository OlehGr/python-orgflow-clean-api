from dataclasses import dataclass

from app.core.application.interfaces.repository.entity_event import IEntityEventRepository
from app.core.models import EntityEventModel
from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class EntityEventRepository(IEntityEventRepository):
    _tm: TransactionManager

    async def save(self, event: EntityEventModel) -> None:
        async with self._tm.transaction() as tx:
            await tx.merge(event)
