import uuid
from typing import Unpack

from sqlalchemy import Select, select

from app.core.application.dto.organization_member import OrganizationMembersGetParams
from app.core.models import OrganizationMemberModel
from app.infrastructure.database.builders.base import BaseSelectBuilder
from app.infrastructure.database.builders.organization import OrganizationSelectBuilder


SelectOrganizationMemberModel = Select[tuple[OrganizationMemberModel]]


class OrganizationMemberSelectBuilder(BaseSelectBuilder):
    @classmethod
    def build_get_all_select(
        cls, *, actor_id: uuid.UUID | None, **kwargs: Unpack[OrganizationMembersGetParams]
    ) -> SelectOrganizationMemberModel:
        query = select(OrganizationMemberModel)
        return cls.with_get_all_where_conditions(query, actor_id=actor_id, **kwargs).order_by(
            OrganizationMemberModel.created_at.desc()
        )

    @classmethod
    def with_get_all_where_conditions(
        cls,
        query: Select,
        *,
        actor_id: uuid.UUID | None,
        organization_member__organization_id: uuid.UUID | None = None,
        organization_member__user_id: uuid.UUID | None = None,
    ) -> Select:
        if organization_member__organization_id is not None:
            query = query.where(OrganizationMemberModel.organization_id == organization_member__organization_id)
        if organization_member__user_id is not None:
            query = query.where(OrganizationMemberModel.user_id == organization_member__user_id)

        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_get_by_id_select(
        cls, organization_member_id: uuid.UUID, actor_id: uuid.UUID | None
    ) -> SelectOrganizationMemberModel:
        query = select(OrganizationMemberModel).where(OrganizationMemberModel.id == organization_member_id).limit(1)
        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_actor_organization_member_ids_select(cls, actor_id: uuid.UUID) -> Select:
        actor_organization_ids_cte = OrganizationSelectBuilder.build_actor_organization_ids_select(actor_id).cte()

        return select(OrganizationMemberModel.id.label("organization_member_id")).join(
            actor_organization_ids_cte,
            actor_organization_ids_cte.c.organization_id == OrganizationMemberModel.organization_id,
        )

    @classmethod
    def with_actor_where_conditions(cls, query: Select, actor_id: uuid.UUID | None) -> Select:
        if actor_id is None:
            return query

        actor_organization_member_ids_cte = cls.build_actor_organization_member_ids_select(actor_id).cte()

        return query.join(
            actor_organization_member_ids_cte,
            actor_organization_member_ids_cte.c.organization_member_id == OrganizationMemberModel.id,
        )
