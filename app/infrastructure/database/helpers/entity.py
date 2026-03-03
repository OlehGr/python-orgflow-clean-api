import uuid
from typing import TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.dto.user import UserAvatarReadDto
from app.core.models import BaseModel, FileModel, UserModel


TModel = TypeVar("TModel", bound=BaseModel)


class EntitiesLoadHelper:
    @classmethod
    async def load_models(cls, query: Select[tuple[TModel]], session: AsyncSession) -> tuple[TModel, ...]:
        query_result = await session.scalars(query)
        return tuple(query_result.all())

    @classmethod
    async def load_users(cls, user_ids: set[uuid.UUID], session: AsyncSession) -> tuple[UserModel, ...]:
        return await cls.load_models(select(UserModel).where(UserModel.id.in_(user_ids)), session)

    @classmethod
    async def load_users_map(cls, user_ids: set[uuid.UUID], session: AsyncSession) -> dict[uuid.UUID, UserModel]:
        users = await cls.load_users(user_ids, session)
        return {user.id: user for user in users}

    @classmethod
    async def load_user_avatar_reads_map(
        cls, file_ids: set[uuid.UUID], session: AsyncSession
    ) -> dict[uuid.UUID, UserAvatarReadDto]:
        files = await cls.load_files(file_ids, session)
        return {file.id: UserAvatarReadDto.from_file(file) for file in files}

    @classmethod
    async def load_files(cls, file_ids: set[uuid.UUID], session: AsyncSession) -> tuple[FileModel, ...]:
        return await cls.load_models(select(FileModel).where(FileModel.id.in_(file_ids)), session)

    @classmethod
    async def load_files_map(cls, file_ids: set[uuid.UUID], session: AsyncSession) -> dict[uuid.UUID, FileModel]:
        files = await cls.load_files(file_ids, session)
        return {file.id: file for file in files}
