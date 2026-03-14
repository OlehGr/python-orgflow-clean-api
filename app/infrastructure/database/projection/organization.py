import uuid
from dataclasses import dataclass
from typing import Unpack

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.organization import (
    OrganizationReadDto,
    OrganizationSettingsReadDto,
    OrganizationsGetParams,
)
from app.core.application.interfaces.projection.organization import (
    IOrganizationProjection,
    IOrganizationSettingsProjection,
)
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models import OrganizationModel
from app.infrastructure.database.builders.organization import (
    OrganizationSelectBuilder,
    OrganizationSettingsSelectBuilder,
)
from app.infrastructure.database.helpers.data import DataLoadHelper
from app.infrastructure.database.internal.transaction.manager import TransactionManager


@dataclass
class OrganizationProjection(IOrganizationProjection):
    _tm: TransactionManager

    async def get_paged(
        self, actor_id: uuid.UUID, page: int = 1, limit: int = 50, **kwargs: Unpack[OrganizationsGetParams]
    ) -> Paged[OrganizationReadDto]:
        plain_query = OrganizationSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)
        paged_query = OrganizationSelectBuilder.with_paged_limit(plain_query, page=page, limit=limit)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(paged_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paged.to_paged(reads, page=page, limit=limit)

    async def get_paginated(
        self, actor_id: uuid.UUID, page: int = 1, limit: int = 50, **kwargs: Unpack[OrganizationsGetParams]
    ) -> Paginated[OrganizationReadDto]:
        plain_query = OrganizationSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)
        paginated_query = OrganizationSelectBuilder.with_pagination(plain_query, page=page, limit=limit)
        count_query = OrganizationSelectBuilder.to_count_query(
            OrganizationSelectBuilder.with_get_all_where_conditions(
                select(OrganizationModel.id), actor_id=actor_id, **kwargs
            )
        )

        async with self._tm.session() as session:
            count = await session.scalar(count_query) or 0
            entities = await DataLoadHelper.load_models_list(paginated_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paginated.to_paginated(reads, page=page, limit=limit, count=count)

    async def get_by_id(self, organization_id: uuid.UUID, *, actor_id: uuid.UUID | None) -> OrganizationReadDto:
        query = OrganizationSelectBuilder.build_get_by_id_select(organization_id, actor_id)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(query, session)
            reads = await self._load_reads_from_models(entities, session)
            if not reads:
                raise EntityNotFoundError("Organization")
            return reads[0]

    async def _load_reads_from_models(
        self, organizations: list[OrganizationModel], _session: AsyncSession
    ) -> list[OrganizationReadDto]:

        return [
            OrganizationReadDto.from_organization(
                organization,
            )
            for organization in organizations
        ]


@dataclass
class OrganizationSettingsProjection(IOrganizationSettingsProjection):
    _tm: TransactionManager

    async def get_by_id(self, organization_id: uuid.UUID, *, actor_id: uuid.UUID | None) -> OrganizationSettingsReadDto:
        query = OrganizationSettingsSelectBuilder.build_get_by_id_select(organization_id, actor_id)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(query, session)
            reads = await self._load_reads_from_models(entities, session)
            if not reads:
                raise EntityNotFoundError("Organization Settings")
            return reads[0]

    async def _load_reads_from_models(
        self, organizations: list[OrganizationModel], _session: AsyncSession
    ) -> list[OrganizationSettingsReadDto]:

        return [
            OrganizationSettingsReadDto.from_organization(
                organization,
            )
            for organization in organizations
        ]
