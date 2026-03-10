import uuid
from dataclasses import dataclass

from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.repository.file import IFileRepository
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models import FileModel
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject
from app.core.models.file import FileEventDto
from app.infrastructure.database.builders.file import FileSelectBuilder
from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class FileRepository(IFileRepository):
    _tm: TransactionManager
    _entity_event_bus: IEntityEventBus

    async def save(self, file: FileModel, *, actor_id: uuid.UUID | None) -> None:
        async with self._tm.transaction() as tx:
            await tx.merge(file)
            tx.add_async_after_commit(lambda: self._public_save_event(file, actor_id))

    async def get_by_id(self, file_id: uuid.UUID) -> FileModel:
        query = FileSelectBuilder.build_get_by_id_select(file_id)

        async with self._tm.session() as session:
            entity = await session.scalar(query)
            if not entity:
                raise EntityNotFoundError("File")
            return entity

    async def _public_save_event(self, file: FileModel, actor_id: uuid.UUID | None) -> None:
        await self._entity_event_bus.publish(
            EntityEvent(
                producer_id=actor_id,
                subject=EntityEventSubject.file_save,
                entity=EntityEventEntity.file,
                entity_id=file.id,
                data=FileEventDto.from_file(file),
            )
        )
