import uuid
from typing import Unpack

from sqlalchemy import Select, select

from app.core.application.dto.organization import OrganizationsGetParams
from app.core.models import OrganizationMemberModel, OrganizationModel
from app.core.models.organization_member import OrganizationMemberRole
from app.infrastructure.database.builders.base import BaseSelectBuilder


SelectOrganizationModel = Select[tuple[OrganizationModel]]


class OrganizationSelectBuilder(BaseSelectBuilder):
    @classmethod
    def build_get_all_select(
        cls, *, actor_id: uuid.UUID | None, **kwargs: Unpack[OrganizationsGetParams]
    ) -> SelectOrganizationModel:
        query = select(OrganizationModel)
        return cls.with_get_all_where_conditions(query, actor_id=actor_id, **kwargs).order_by(
            OrganizationModel.created_at.desc()
        )

    @classmethod
    def with_get_all_where_conditions(
        cls, query: Select, *, actor_id: uuid.UUID | None, organization__id: set[uuid.UUID] | None = None
    ) -> Select:
        if organization__id is not None:
            query = query.where(OrganizationModel.id.in_(organization__id))

        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_get_by_id_select(cls, organization_id: uuid.UUID, actor_id: uuid.UUID | None) -> SelectOrganizationModel:
        query = select(OrganizationModel).where(OrganizationModel.id == organization_id).limit(1)
        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_actor_organization_ids_select(cls, actor_id: uuid.UUID) -> Select:
        return select(OrganizationMemberModel.organization_id).where(OrganizationMemberModel.user_id == actor_id)

    @classmethod
    def with_actor_where_conditions(cls, query: Select, actor_id: uuid.UUID | None) -> Select:
        if actor_id is None:
            return query

        actor_organization_ids_cte = cls.build_actor_organization_ids_select(actor_id).cte()

        return query.join(
            actor_organization_ids_cte, actor_organization_ids_cte.c.organization_id == OrganizationModel.id
        )

    @classmethod
    def build_actor_organization_settings_ids_select(cls, actor_id: uuid.UUID) -> Select:
        return select(OrganizationMemberModel.organization_id).where(
            OrganizationMemberModel.user_id == actor_id, OrganizationMemberModel.role == OrganizationMemberRole.ADMIN
        )

    @classmethod
    def with_actor_organization_settings_where_conditions(cls, query: Select, actor_id: uuid.UUID | None) -> Select:
        if actor_id is None:
            return query

        actor_organization_ids_cte = cls.build_actor_organization_settings_ids_select(actor_id).cte()

        return query.join(
            actor_organization_ids_cte, actor_organization_ids_cte.c.organization_id == OrganizationModel.id
        )


class OrganizationSettingsSelectBuilder(BaseSelectBuilder):
    @classmethod
    def build_get_by_id_select(cls, organization_id: uuid.UUID, actor_id: uuid.UUID | None) -> SelectOrganizationModel:
        query = select(OrganizationModel).where(OrganizationModel.id == organization_id).limit(1)
        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_actor_organization_settings_ids_select(cls, actor_id: uuid.UUID) -> Select:
        return select(OrganizationMemberModel.organization_id).where(
            OrganizationMemberModel.user_id == actor_id, OrganizationMemberModel.role == OrganizationMemberRole.ADMIN
        )

    @classmethod
    def with_actor_where_conditions(cls, query: Select, actor_id: uuid.UUID | None) -> Select:
        if actor_id is None:
            return query

        actor_organization_ids_cte = cls.build_actor_organization_settings_ids_select(actor_id).cte()

        return query.join(
            actor_organization_ids_cte, actor_organization_ids_cte.c.organization_id == OrganizationModel.id
        )
