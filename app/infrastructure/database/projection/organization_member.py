import uuid
from dataclasses import dataclass
from typing import Unpack

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.organization_member import OrganizationMemberReadDto, OrganizationMembersGetParams
from app.core.application.interfaces.projection.organization_member import IOrganizationMemberProjection
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models import OrganizationMemberModel
from app.infrastructure.database.builders.organization_member import OrganizationMemberSelectBuilder
from app.infrastructure.database.helpers.data import DataLoadHelper
from app.infrastructure.database.helpers.entity import EntitiesLoadHelper
from app.infrastructure.database.internal.transaction.manager import TransactionManager


@dataclass
class OrganizationMemberProjection(IOrganizationMemberProjection):
    _tm: TransactionManager

    async def get_paged(
        self, actor_id: uuid.UUID, page: int = 1, limit: int = 50, **kwargs: Unpack[OrganizationMembersGetParams]
    ) -> Paged[OrganizationMemberReadDto]:
        plain_query = OrganizationMemberSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)
        paged_query = OrganizationMemberSelectBuilder.with_paged_limit(plain_query, page=page, limit=limit)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(paged_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paged.to_paged(reads, page=page, limit=limit)

    async def get_paginated(
        self, actor_id: uuid.UUID, page: int = 1, limit: int = 50, **kwargs: Unpack[OrganizationMembersGetParams]
    ) -> Paginated[OrganizationMemberReadDto]:
        plain_query = OrganizationMemberSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)
        paginated_query = OrganizationMemberSelectBuilder.with_pagination(plain_query, page=page, limit=limit)
        count_query = OrganizationMemberSelectBuilder.to_count_query(
            OrganizationMemberSelectBuilder.with_get_all_where_conditions(
                select(OrganizationMemberModel.id), actor_id=actor_id, **kwargs
            )
        )

        async with self._tm.session() as session:
            count = await session.scalar(count_query) or 0
            entities = await DataLoadHelper.load_models_list(paginated_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paginated.to_paginated(reads, page=page, limit=limit, count=count)

    async def get_by_id(
        self, organization_member_id: uuid.UUID, *, actor_id: uuid.UUID | None
    ) -> OrganizationMemberReadDto:
        query = OrganizationMemberSelectBuilder.build_get_by_id_select(organization_member_id, actor_id)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(query, session)
            reads = await self._load_reads_from_models(entities, session)
            if not reads:
                raise EntityNotFoundError("OrganizationMember")
            return reads[0]

    async def _load_reads_from_models(
        self, organization_members: list[OrganizationMemberModel], session: AsyncSession
    ) -> list[OrganizationMemberReadDto]:

        user_reads_map = await EntitiesLoadHelper.load_user_reads_map(
            {organization_member.user_id for organization_member in organization_members}, session
        )

        return [
            OrganizationMemberReadDto.from_organization_member(
                organization_member, user=user_reads_map[organization_member.user_id]
            )
            for organization_member in organization_members
        ]
