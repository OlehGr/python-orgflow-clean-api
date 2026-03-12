import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.organization_member import OrganizationMembersGetParams
from app.core.models import OrganizationMemberModel


class IOrganizationMemberRepository(Protocol):
    @abstractmethod
    async def save(self, organization_member: OrganizationMemberModel, *, actor_id: uuid.UUID | None) -> None: ...

    @abstractmethod
    async def delete(self, organization_member: OrganizationMemberModel, *, actor_id: uuid.UUID | None) -> None: ...

    @abstractmethod
    async def get_all(
        self, *, actor_id: uuid.UUID | None = None, **kwargs: Unpack[OrganizationMembersGetParams]
    ) -> list[OrganizationMemberModel]: ...

    @abstractmethod
    async def get_by_id(
        self, organization_member_id: uuid.UUID, *, actor_id: uuid.UUID | None = None
    ) -> OrganizationMemberModel: ...

    @abstractmethod
    async def get_user_organization_member(
        self, *, user_id: uuid.UUID, organization_id: uuid.UUID
    ) -> OrganizationMemberModel: ...
