import uuid
from dataclasses import dataclass
from typing import Unpack

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.project import ProjectReadDto, ProjectsGetParams
from app.core.application.interfaces.projection.project import IProjectProjection
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models import ProjectModel
from app.infrastructure.database.builders.project import ProjectSelectBuilder
from app.infrastructure.database.helpers.data import DataLoadHelper
from app.infrastructure.database.helpers.entity import EntitiesLoadHelper
from app.infrastructure.database.internal.transaction.manager import TransactionManager


@dataclass
class ProjectProjection(IProjectProjection):
    _tm: TransactionManager

    async def get_paged(
        self, actor_id: uuid.UUID, page: int = 1, limit: int = 50, **kwargs: Unpack[ProjectsGetParams]
    ) -> Paged[ProjectReadDto]:
        plain_query = ProjectSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)
        paged_query = ProjectSelectBuilder.with_paged_limit(plain_query, page=page, limit=limit)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(paged_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paged.to_paged(reads, page=page, limit=limit)

    async def get_paginated(
        self, actor_id: uuid.UUID, page: int = 1, limit: int = 50, **kwargs: Unpack[ProjectsGetParams]
    ) -> Paginated[ProjectReadDto]:
        plain_query = ProjectSelectBuilder.build_get_all_select(actor_id=actor_id, **kwargs)
        paginated_query = ProjectSelectBuilder.with_pagination(plain_query, page=page, limit=limit)
        count_query = ProjectSelectBuilder.to_count_query(
            ProjectSelectBuilder.with_get_all_where_conditions(select(ProjectModel.id), actor_id=actor_id, **kwargs)
        )

        async with self._tm.session() as session:
            count = await session.scalar(count_query) or 0
            entities = await DataLoadHelper.load_models_list(paginated_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paginated.to_paginated(reads, page=page, limit=limit, count=count)

    async def get_by_id(self, project_id: uuid.UUID, *, actor_id: uuid.UUID | None) -> ProjectReadDto:
        query = ProjectSelectBuilder.build_get_by_id_select(project_id, actor_id)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(query, session)
            reads = await self._load_reads_from_models(entities, session)
            if not reads:
                raise EntityNotFoundError("Project")
            return reads[0]

    async def _load_reads_from_models(
        self, projects: list[ProjectModel], session: AsyncSession
    ) -> list[ProjectReadDto]:

        organization_ids: set[uuid.UUID] = set()
        user_ids: set[uuid.UUID] = set()

        for project in projects:
            organization_ids.add(project.organization_id)
            if project.author_id:
                user_ids.add(project.author_id)

        organization_reads_map = await EntitiesLoadHelper.load_organization_reads_map(organization_ids, session)
        user_reads_map = await EntitiesLoadHelper.load_user_reads_map(user_ids, session)

        return [
            ProjectReadDto.from_project(
                project,
                organization=organization_reads_map[project.organization_id],
                author=user_reads_map[project.author_id] if project.author_id else None,
            )
            for project in projects
        ]
