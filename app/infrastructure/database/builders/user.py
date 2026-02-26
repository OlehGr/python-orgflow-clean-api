from typing import TYPE_CHECKING, Unpack

from sqlalchemy import Select, select

from app.core.models import UserModel
from app.infrastructure.database.builders.base import BaseSelectBuilder


if TYPE_CHECKING:
    import uuid

    from app.core.application.dto.user import UsersGetParams

SelectUserModel = Select[tuple[UserModel]]


class UserSelectBuilder(BaseSelectBuilder):
    @classmethod
    def build_get_all_select(cls, **kwargs: Unpack[UsersGetParams]) -> SelectUserModel:
        query = select(UserModel)
        return cls.with_get_all_where_conditions(query, **kwargs)

    @classmethod
    def with_get_all_where_conditions(cls, query: Select, *, user__normal_email: str | None = None) -> Select:
        if user__normal_email is not None:
            query = query.where(UserModel.email == user__normal_email)

        return query

    @classmethod
    def build_get_by_id_select(cls, user_id: uuid.UUID) -> SelectUserModel:
        return select(UserModel).where(UserModel.id == user_id).limit(1)
