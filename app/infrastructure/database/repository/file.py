import uuid
from dataclasses import dataclass

from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.repository.file import IFileRepository
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models import FileModel
from app.infrastructure.database.builders.file import FileSelectBuilder
from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class FileRepository(IFileRepository):
    _tm: TransactionManager
    _entity_event_bus: IEntityEventBus

    async def save(self, file: FileModel, *, actor_id: uuid.UUID | None) -> None:
        async with self._tm.transaction() as tx:
            await tx.merge(file)
            tx.add_async_after_commit(
                lambda: self._entity_event_bus.publish(file.to_entity_save_event(producer_id=actor_id))
            )

    async def get_by_id(self, file_id: uuid.UUID) -> FileModel:
        query = FileSelectBuilder.build_get_by_id_select(file_id)

        async with self._tm.session() as session:
            entity = await session.scalar(query)
            if not entity:
                raise EntityNotFoundError("File")
            return entity
