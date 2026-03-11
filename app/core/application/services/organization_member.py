import uuid
from dataclasses import dataclass

from app.core.application.dto.organization_member import (
    OrganizationMemberCreateDto,
    OrganizationMemberUpdateRoleDto,
)
from app.core.application.interfaces.repository.organization_member import IOrganizationMemberRepository
from app.core.models import OrganizationMemberModel


@dataclass
class OrganizationMemberService:
    _organization_member_repository: IOrganizationMemberRepository

    async def create_organization_member(
        self, data: OrganizationMemberCreateDto, *, actor_id: uuid.UUID | None
    ) -> uuid.UUID:
        organization_member = OrganizationMemberModel.create(
            user_id=data.user_id, organization_id=data.organization_id, role=data.role
        )

        await self._organization_member_repository.save(organization_member, actor_id=actor_id)

        return organization_member.id

    async def update_organization_member_role(
        self, organization_id: uuid.UUID, data: OrganizationMemberUpdateRoleDto, *, actor_id: uuid.UUID | None
    ) -> None:
        organization_member = await self._organization_member_repository.get_by_id(organization_id)

        organization_member.set_role(data.role)

        await self._organization_member_repository.save(organization_member, actor_id=actor_id)

    async def delete_organization_member(self, organization_member_id: uuid.UUID, *, actor_id: uuid.UUID) -> None:
        organization_member = await self._organization_member_repository.get_by_id(organization_member_id)
        await self._organization_member_repository.delete(organization_member, actor_id=actor_id)
