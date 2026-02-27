import uuid
from dataclasses import dataclass
from typing import Unpack

from app.core.application.dto.user import UsersGetParams
from app.core.application.interfaces.repository.user import IUserRepository
from app.core.exceptions.entity import EntityNotFoundError
from app.core.models.user import UserModel
from app.infrastructure.database.builders.user import UserSelectBuilder
from app.infrastructure.database.helpers.data import DataLoadHelper
from app.infrastructure.database.internal.transaction import TransactionManager


@dataclass
class UserRepository(IUserRepository):
    _tm: TransactionManager

    async def save(self, user: UserModel) -> None:
        async with self._tm.transaction() as tx:
            await tx.merge(user)

    async def get_all(self, **kwargs: Unpack[UsersGetParams]) -> list[UserModel]:
        query = UserSelectBuilder.build_get_all_select(**kwargs)

        async with self._tm.session() as session:
            return await DataLoadHelper.load_models_list(query, session)

    async def get_by_id(self, user_id: uuid.UUID) -> UserModel:
        query = UserSelectBuilder.build_get_by_id_select(user_id)

        async with self._tm.session() as session:
            entity = await session.scalar(query)
            if not entity:
                raise EntityNotFoundError("User")
            return entity
