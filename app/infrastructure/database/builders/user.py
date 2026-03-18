import uuid
from typing import Unpack

from sqlalchemy import Select, literal_column, select, union

from app.core.application.dto.user import UsersGetParams
from app.core.models import OrganizationMemberModel, UserModel
from app.infrastructure.database.builders.base import BaseSelectBuilder


SelectUserModel = Select[tuple[UserModel]]


class UserSelectBuilder(BaseSelectBuilder):
    @classmethod
    def build_get_all_select(cls, *, actor_id: uuid.UUID | None, **kwargs: Unpack[UsersGetParams]) -> SelectUserModel:
        query = select(UserModel)
        return cls.with_get_all_where_conditions(query, actor_id=actor_id, **kwargs).order_by(
            UserModel.created_at.desc()
        )

    @classmethod
    def with_get_all_where_conditions(
        cls, query: Select, *, actor_id: uuid.UUID | None, user__normal_email: str | None = None
    ) -> Select:
        if user__normal_email is not None:
            query = query.where(UserModel.email == user__normal_email)

        return cls.with_actor_where_conditions(query, actor_id)

    @classmethod
    def build_actor_user_ids_select(cls, actor_id: uuid.UUID) -> Select:
        actor_organization_ids_cte = (
            select(OrganizationMemberModel.organization_id).where(OrganizationMemberModel.user_id == actor_id).cte()
        )

        organizations_user_ids_select = select(OrganizationMemberModel.user_id).join(
            actor_organization_ids_cte,
            actor_organization_ids_cte.c.organization_id == OrganizationMemberModel.organization_id,
        )

        actor_user_id_select = select(UserModel.id.label("user_id")).where(UserModel.id == actor_id)

        return select(literal_column("user_id")).select_from(
            union(organizations_user_ids_select, actor_user_id_select).subquery()
        )

    @classmethod
    def with_actor_where_conditions(cls, query: Select, actor_id: uuid.UUID | None) -> Select:
        if actor_id is None:
            return query

        actor_user_ids_cte = cls.build_actor_user_ids_select(actor_id).cte()

        return query.join(actor_user_ids_cte, actor_user_ids_cte.c.user_id == UserModel.id)

    @classmethod
    def build_get_by_id_select(cls, user_id: uuid.UUID) -> SelectUserModel:
        return select(UserModel).where(UserModel.id == user_id).limit(1)
