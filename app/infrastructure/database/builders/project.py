import uuid
from typing import Unpack

from sqlalchemy import Select, select

from app.core.application.dto.project import ProjectsGetParams
from app.core.models import ProjectModel
from app.infrastructure.database.builders.base import BaseSelectBuilder
from app.infrastructure.database.builders.organization import OrganizationSelectBuilder


SelectProjectModel = Select[tuple[ProjectModel]]


class ProjectSelectBuilder(BaseSelectBuilder):
    @classmethod
    def build_get_all_select(
        cls, *, actor_id: uuid.UUID | None, **kwargs: Unpack[ProjectsGetParams]
    ) -> SelectProjectModel:
        query = select(ProjectModel)
        return cls.with_get_all_where_conditions(query, actor_id=actor_id, **kwargs).order_by(
            ProjectModel.created_at.desc()
        )

    @classmethod
    def with_get_all_where_conditions(
        cls, query: Select, *, actor_id: uuid.UUID | None, project__id: set[uuid.UUID] | None = None
    ) -> Select:
        if project__id is not None:
            query = query.where(ProjectModel.id.in_(project__id))

        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_get_by_id_select(cls, project_id: uuid.UUID, actor_id: uuid.UUID | None) -> SelectProjectModel:
        query = select(ProjectModel).where(ProjectModel.id == project_id).limit(1)
        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_actor_project_ids_select(cls, actor_id: uuid.UUID) -> Select:
        actor_organization_ids_cte = OrganizationSelectBuilder.build_actor_organization_ids_select(actor_id).cte()

        return select(ProjectModel.id.label("project_id")).join(
            actor_organization_ids_cte, actor_organization_ids_cte.c.organization_id == ProjectModel.organization_id
        )

    @classmethod
    def with_actor_where_conditions(cls, query: Select, actor_id: uuid.UUID | None) -> Select:
        if actor_id is None:
            return query

        actor_project_ids_cte = cls.build_actor_project_ids_select(actor_id).cte()

        return query.join(actor_project_ids_cte, actor_project_ids_cte.c.project_id == ProjectModel.id)
