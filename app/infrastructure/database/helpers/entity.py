import uuid
from typing import TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.dto.organization import OrganizationReadDto
from app.core.application.dto.user import UserAvatarReadDto, UserReadDto
from app.core.models import BaseModel, FileModel, OrganizationModel, UserModel


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
    async def load_user_avatar_reads_map(
        cls, file_ids: set[uuid.UUID], session: AsyncSession
    ) -> dict[uuid.UUID, UserAvatarReadDto]:
        files = await cls.load_files(file_ids, session)
        return {file.id: UserAvatarReadDto.from_file(file) for file in files}

    @classmethod
    async def load_user_reads_map(cls, user_ids: set[uuid.UUID], session: AsyncSession) -> dict[uuid.UUID, UserReadDto]:
        users = await cls.load_users(user_ids, session)
        user_avatar_reads_map = await cls.load_user_avatar_reads_map(
            {user.avatar_file_id for user in users if user.avatar_file_id}, session
        )
        return {
            user.id: UserReadDto.from_user(
                user, avatar=user_avatar_reads_map[user.avatar_file_id] if user.avatar_file_id else None
            )
            for user in users
        }

    @classmethod
    async def load_files(cls, file_ids: set[uuid.UUID], session: AsyncSession) -> tuple[FileModel, ...]:
        return await cls.load_models(select(FileModel).where(FileModel.id.in_(file_ids)), session)

    @classmethod
    async def load_files_map(cls, file_ids: set[uuid.UUID], session: AsyncSession) -> dict[uuid.UUID, FileModel]:
        files = await cls.load_files(file_ids, session)
        return {file.id: file for file in files}

    @classmethod
    async def load_organizations(
        cls, organization_ids: set[uuid.UUID], session: AsyncSession
    ) -> tuple[OrganizationModel, ...]:
        return await cls.load_models(
            select(OrganizationModel).where(OrganizationModel.id.in_(organization_ids)), session
        )

    @classmethod
    async def load_organization_reads_map(
        cls, organization_ids: set[uuid.UUID], session: AsyncSession
    ) -> dict[uuid.UUID, OrganizationReadDto]:
        organizations = await cls.load_organizations(organization_ids, session)
        return {organization.id: OrganizationReadDto.from_organization(organization) for organization in organizations}
