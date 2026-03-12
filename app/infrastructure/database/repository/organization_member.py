import uuid
from dataclasses import dataclass
from typing import Unpack

from app.core.application.dto.organization_member import OrganizationMembersGetParams
from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.repository.organization_member import IOrganizationMemberRepository
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject
from app.core.models.organization_member import OrganizationMemberEventDto, OrganizationMemberModel
from app.infrastructure.database.builders.organization_member import OrganizationMemberSelectBuilder
from app.infrastructure.database.helpers.data import DataLoadHelper
from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class OrganizationMemberRepository(IOrganizationMemberRepository):
    _tm: TransactionManager
    _entity_event_bus: IEntityEventBus

    async def get_all(
        self, actor_id: uuid.UUID | None = None, **kwargs: Unpack[OrganizationMembersGetParams]
    ) -> list[OrganizationMemberModel]:
        query = OrganizationMemberSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)

        async with self._tm.session() as session:
            return await DataLoadHelper.load_models_list(query, session)

    async def get_by_id(
        self, organization_member_id: uuid.UUID, *, actor_id: uuid.UUID | None = None
    ) -> OrganizationMemberModel:
        query = OrganizationMemberSelectBuilder.build_get_by_id_select(organization_member_id, actor_id)

        async with self._tm.session() as session:
            entity = await session.scalar(query)
            if not entity:
                raise EntityNotFoundError("OrganizationMember")
            return entity

    async def save(self, organization_member: OrganizationMemberModel, *, actor_id: uuid.UUID | None) -> None:
        async with self._tm.transaction() as tx:
            await tx.merge(organization_member)
            tx.add_async_after_commit(
                lambda: self._entity_event_bus.publish(
                    EntityEvent(
                        producer_id=actor_id,
                        subject=EntityEventSubject.organization_member_save,
                        entity=EntityEventEntity.organization_member,
                        entity_id=organization_member.id,
                        data=OrganizationMemberEventDto.from_organization_member(organization_member),
                    )
                )
            )

    async def delete(self, organization_member: OrganizationMemberModel, *, actor_id: uuid.UUID | None) -> None:
        async with self._tm.transaction() as tx:
            await tx.delete(organization_member)
            tx.add_async_after_commit(
                lambda: self._entity_event_bus.publish(
                    EntityEvent(
                        producer_id=actor_id,
                        subject=EntityEventSubject.organization_member_delete,
                        entity=EntityEventEntity.organization_member,
                        entity_id=organization_member.id,
                        data=OrganizationMemberEventDto.from_organization_member(organization_member),
                    )
                )
            )
