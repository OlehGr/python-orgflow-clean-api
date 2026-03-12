import uuid
from typing import NotRequired, TypedDict

import msgspec

from app.core.application.dto.base import LimitationGetParams
from app.core.application.dto.user import UserReadDto
from app.core.models import OrganizationMemberModel
from app.core.models.base import EntityDto
from app.core.models.organization_member import OrganizationMemberRole


class OrganizationMembersGetParams(TypedDict):
    organization_member__organization_id: NotRequired[uuid.UUID | None]
    organization_member__user_id: NotRequired[uuid.UUID | None]


class OrganizationMembersWithLimitationGetParams(OrganizationMembersGetParams, LimitationGetParams): ...


class OrganizationMemberReadDto(EntityDto, frozen=True):
    organization_id: uuid.UUID
    user_id: uuid.UUID
    user: UserReadDto
    role: OrganizationMemberRole

    @classmethod
    def from_organization_member(
        cls, organization_member: OrganizationMemberModel, user: UserReadDto
    ) -> "OrganizationMemberReadDto":
        return cls(
            id=organization_member.id,
            created_at=organization_member.created_at,
            updated_at=organization_member.updated_at,
            is_removed=organization_member.is_removed,
            organization_id=organization_member.organization_id,
            role=organization_member.role,
            user_id=organization_member.user_id,
            user=user,
        )


class OrganizationMemberCreateDto(msgspec.Struct, frozen=True):
    organization_id: uuid.UUID
    user_id: uuid.UUID
    role: OrganizationMemberRole = OrganizationMemberRole.MEMBER


class OrganizationMemberUpdateRoleDto(msgspec.Struct, frozen=True):
    role: OrganizationMemberRole
