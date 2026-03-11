import uuid
from dataclasses import dataclass
from typing import Unpack

from app.core.application.dto.organization import OrganizationsGetParams
from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.repository.organization import IOrganizationRepository
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject
from app.core.models.organization import OrganizationEventDto, OrganizationModel
from app.infrastructure.database.builders.organization import OrganizationSelectBuilder
from app.infrastructure.database.helpers.data import DataLoadHelper
from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class OrganizationRepository(IOrganizationRepository):
    _tm: TransactionManager
    _entity_event_bus: IEntityEventBus

    async def get_all(
        self, actor_id: uuid.UUID | None = None, **kwargs: Unpack[OrganizationsGetParams]
    ) -> list[OrganizationModel]:
        query = OrganizationSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)

        async with self._tm.session() as session:
            return await DataLoadHelper.load_models_list(query, session)

    async def get_by_id(self, organization_id: uuid.UUID, *, actor_id: uuid.UUID | None = None) -> OrganizationModel:
        query = OrganizationSelectBuilder.build_get_by_id_select(organization_id, actor_id)

        async with self._tm.session() as session:
            entity = await session.scalar(query)
            if not entity:
                raise EntityNotFoundError("Organization")
            return entity

    async def save(self, organization: OrganizationModel, *, actor_id: uuid.UUID | None) -> None:
        async with self._tm.transaction() as tx:
            await tx.merge(organization)
            tx.add_async_after_commit(lambda: self._public_save_event(organization, actor_id))

    async def _public_save_event(self, organization: OrganizationModel, actor_id: uuid.UUID | None) -> None:
        await self._entity_event_bus.publish(
            EntityEvent(
                producer_id=actor_id,
                subject=EntityEventSubject.organization_save,
                entity=EntityEventEntity.organization,
                entity_id=organization.id,
                data=OrganizationEventDto.from_organization(organization),
            )
        )
