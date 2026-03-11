import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.organization_member import (
    OrganizationMemberReadDto,
    OrganizationMembersWithLimitationGetParams,
)


class IOrganizationMemberProjection(Protocol):
    @abstractmethod
    async def get_by_id(
        self, organization_member_id: uuid.UUID, *, actor_id: uuid.UUID | None
    ) -> OrganizationMemberReadDto: ...

    @abstractmethod
    async def get_paged(
        self, *, actor_id: uuid.UUID, **kwargs: Unpack[OrganizationMembersWithLimitationGetParams]
    ) -> Paged[OrganizationMemberReadDto]: ...

    @abstractmethod
    async def get_paginated(
        self, *, actor_id: uuid.UUID, **kwargs: Unpack[OrganizationMembersWithLimitationGetParams]
    ) -> Paginated[OrganizationMemberReadDto]: ...
