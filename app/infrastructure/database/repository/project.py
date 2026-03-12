import uuid
from dataclasses import dataclass
from typing import Unpack

from app.core.application.dto.project import ProjectsGetParams
from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.repository.project import IProjectRepository
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject
from app.core.models.project import ProjectEventDto, ProjectModel
from app.infrastructure.database.builders.project import ProjectSelectBuilder
from app.infrastructure.database.helpers.data import DataLoadHelper
from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class ProjectRepository(IProjectRepository):
    _tm: TransactionManager
    _entity_event_bus: IEntityEventBus

    async def get_all(
        self, actor_id: uuid.UUID | None = None, **kwargs: Unpack[ProjectsGetParams]
    ) -> list[ProjectModel]:
        query = ProjectSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)

        async with self._tm.session() as session:
            return await DataLoadHelper.load_models_list(query, session)

    async def get_by_id(self, project_id: uuid.UUID, *, actor_id: uuid.UUID | None = None) -> ProjectModel:
        query = ProjectSelectBuilder.build_get_by_id_select(project_id, actor_id)

        async with self._tm.session() as session:
            entity = await session.scalar(query)
            if not entity:
                raise EntityNotFoundError("Project")
            return entity

    async def save(self, project: ProjectModel, *, actor_id: uuid.UUID | None) -> None:
        async with self._tm.transaction() as tx:
            await tx.merge(project)
            tx.add_async_after_commit(
                lambda: self._entity_event_bus.publish(
                    EntityEvent(
                        producer_id=actor_id,
                        subject=EntityEventSubject.project_save,
                        entity=EntityEventEntity.project,
                        entity_id=project.id,
                        data=ProjectEventDto.from_project(project),
                    )
                )
            )

    async def delete(self, project: ProjectModel, *, actor_id: uuid.UUID | None) -> None:
        async with self._tm.transaction() as tx:
            await tx.delete(project)
            tx.add_async_after_commit(
                lambda: self._entity_event_bus.publish(
                    EntityEvent(
                        producer_id=actor_id,
                        subject=EntityEventSubject.project_delete,
                        entity=EntityEventEntity.project,
                        entity_id=project.id,
                        data=ProjectEventDto.from_project(project),
                    )
                )
            )
