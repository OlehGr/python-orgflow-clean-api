import uuid
from dataclasses import dataclass

from app.core.application.dto.organization_member import (
    OrganizationMemberCreateDto,
    OrganizationMemberUpdateRoleDto,
)
from app.core.application.interfaces.repository.organization import IOrganizationRepository
from app.core.application.interfaces.repository.organization_member import IOrganizationMemberRepository
from app.core.application.services.permission import PermissionService
from app.core.models import OrganizationMemberModel
from app.core.models.permission import Permission


@dataclass
class OrganizationMemberService:
    _organization_member_repository: IOrganizationMemberRepository
    _organization_repository: IOrganizationRepository

    _permission_service: PermissionService

    async def create_organization_member(self, data: OrganizationMemberCreateDto, *, actor_id: uuid.UUID) -> uuid.UUID:
        organization = await self._organization_repository.get_by_id(data.organization_id)

        if organization.author_id != actor_id:
            await self._permission_service.ensure(
                Permission.ORGANIZATION_MEMBER_CREATE, actor_id=actor_id, organization_id=data.organization_id
            )

        organization_member = OrganizationMemberModel.create(
            user_id=data.user_id, organization_id=data.organization_id, role=data.role
        )

        await self._organization_member_repository.save(organization_member, actor_id=actor_id)

        return organization_member.id

    async def update_organization_member_role(
        self, organization_member_id: uuid.UUID, data: OrganizationMemberUpdateRoleDto, *, actor_id: uuid.UUID
    ) -> None:
        organization_member = await self._organization_member_repository.get_by_id(organization_member_id)

        await self._permission_service.ensure(
            Permission.ORGANIZATION_MEMBER_UPDATE,
            actor_id=actor_id,
            organization_id=organization_member.organization_id,
        )

        organization_member.set_role(data.role)

        await self._organization_member_repository.save(organization_member, actor_id=actor_id)

    async def delete_organization_member(self, organization_member_id: uuid.UUID, *, actor_id: uuid.UUID) -> None:
        organization_member = await self._organization_member_repository.get_by_id(organization_member_id)

        await self._permission_service.ensure(
            Permission.ORGANIZATION_MEMBER_DELETE,
            actor_id=actor_id,
            organization_id=organization_member.organization_id,
        )

        await self._organization_member_repository.delete(organization_member, actor_id=actor_id)
