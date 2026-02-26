from dataclasses import dataclass
from typing import TYPE_CHECKING, Unpack

from sqlalchemy import select

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.user import UserReadDto, UsersGetParams
from app.core.application.interfaces.projection.user import IUserProjection
from app.core.models import UserModel
from app.infrastructure.database.builders.user import UserSelectBuilder
from app.infrastructure.database.helpers.data import DataLoadHelper


if TYPE_CHECKING:
    import uuid

    from sqlalchemy.ext.asyncio import AsyncSession

    from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class UserProjection(IUserProjection):
    _tm: TransactionManager

    async def get_paged(self, page: int = 1, limit: int = 50, **kwargs: Unpack[UsersGetParams]) -> Paged[UserReadDto]:
        plain_query = UserSelectBuilder.build_get_all_select(**kwargs)
        paged_query = UserSelectBuilder.with_paged_limit(plain_query, page=page, limit=limit)

        async with self._tm.session() as session:
            entities = await DataLoadHelper.load_models_list(paged_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paged.to_paged(reads, page=page, limit=limit)

    async def get_paginated(
        self, page: int = 1, limit: int = 50, **kwargs: Unpack[UsersGetParams]
    ) -> Paginated[UserReadDto]:
        plain_query = UserSelectBuilder.build_get_all_select(**kwargs)
        paginated_query = UserSelectBuilder.with_pagination(plain_query, page=page, limit=limit)
        count_query = UserSelectBuilder.to_count_query(
            UserSelectBuilder.with_get_all_where_conditions(select(UserModel.id), **kwargs)
        )

        async with self._tm.session() as session:
            count = await session.scalar(count_query) or 0
            entities = await DataLoadHelper.load_models_list(paginated_query, session)
            reads = await self._load_reads_from_models(entities, session)
            return Paginated.to_paginated(reads, page=page, limit=limit, count=count)

    async def get_by_id(self, user_id: uuid.UUID) -> UserReadDto:
        return await super().get_by_id(user_id)

    async def _load_reads_from_models(self, users: list[UserModel], _session: AsyncSession) -> list[UserReadDto]:
        return [UserReadDto.from_user(user) for user in users]
