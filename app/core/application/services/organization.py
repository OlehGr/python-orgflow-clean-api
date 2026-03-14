import uuid
from dataclasses import dataclass

from app.core.application.dto.organization import OrganizationCreateDto, OrganizationUpdateDto
from app.core.application.dto.organization_member import OrganizationMemberCreateDto
from app.core.application.interfaces.managers.transaction import ITransactionManager
from app.core.application.interfaces.repository.organization import IOrganizationRepository
from app.core.application.interfaces.repository.organization_member import IOrganizationMemberRepository
from app.core.application.services.organization_member import OrganizationMemberService
from app.core.application.services.permission import PermissionService
from app.core.exceptions.validation import ConflictError
from app.core.models import OrganizationModel
from app.core.models.organization_member import OrganizationMemberRole
from app.core.models.permission import Permission


@dataclass
class OrganizationService:
    _tm: ITransactionManager
    _organization_repository: IOrganizationRepository
    _organization_member_repository: IOrganizationMemberRepository

    _organization_member_service: OrganizationMemberService
    _permission_service: PermissionService

    async def create_organization(self, data: OrganizationCreateDto, *, actor_id: uuid.UUID) -> uuid.UUID:
        organization = OrganizationModel.create(name=data.name, author_id=actor_id)

        async with self._tm.transaction():
            await self._organization_repository.save(organization, actor_id=actor_id)

            await self._organization_member_service.create_organization_member(
                OrganizationMemberCreateDto(
                    organization_id=organization.id, user_id=actor_id, role=OrganizationMemberRole.ADMIN
                ),
                actor_id=actor_id,
            )

        return organization.id

    async def update_organization(
        self, organization_id: uuid.UUID, data: OrganizationUpdateDto, *, actor_id: uuid.UUID
    ) -> None:
        await self._permission_service.ensure(
            Permission.ORGANIZATION_UPDATE, actor_id=actor_id, organization_id=organization_id
        )

        organization = await self._organization_repository.get_by_id(organization_id, actor_id=actor_id)

        organization.update(name=data.name)

        await self._organization_repository.save(organization, actor_id=actor_id)

    async def delete_organization(self, organization_id: uuid.UUID, *, actor_id: uuid.UUID) -> None:
        organization = await self._organization_repository.get_by_id(organization_id, actor_id=actor_id)

        if organization.author_id != actor_id:
            raise ConflictError("Только создатель организации может удалить её")

        await self._organization_repository.delete(organization, actor_id=actor_id)

    async def reset_organization_enter_token(self, organization_id: uuid.UUID, *, actor_id: uuid.UUID) -> None:
        await self._permission_service.ensure(
            Permission.ORGANIZATION_UPDATE, actor_id=actor_id, organization_id=organization_id
        )

        organization = await self._organization_repository.get_by_id(organization_id, actor_id=actor_id)

        organization.reset_enter_token()

        await self._organization_repository.save(organization, actor_id=actor_id)

    async def let_user_in_organization(self, *, enter_token: str, actor_id: uuid.UUID) -> uuid.UUID:
        organization = await self._organization_repository.get_by_enter_token(enter_token)

        exist_organization_members = await self._organization_member_repository.get_all(
            organization_member__organization_id=organization.id, organization_member__user_id=actor_id
        )

        if not exist_organization_members:
            await self._organization_member_service.create_organization_member(
                OrganizationMemberCreateDto(
                    organization_id=organization.id, user_id=actor_id, role=OrganizationMemberRole.MEMBER
                ),
                actor_id=None,
            )

        return organization.id
