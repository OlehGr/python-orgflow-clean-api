import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.organization import OrganizationsGetParams
from app.core.models import OrganizationModel


class IOrganizationRepository(Protocol):
    @abstractmethod
    async def save(self, organization: OrganizationModel, *, actor_id: uuid.UUID | None) -> None: ...

    @abstractmethod
    async def delete(self, organization: OrganizationModel, *, actor_id: uuid.UUID | None) -> None: ...

    @abstractmethod
    async def get_all(
        self, *, actor_id: uuid.UUID | None = None, **kwargs: Unpack[OrganizationsGetParams]
    ) -> list[OrganizationModel]: ...

    @abstractmethod
    async def get_by_id(
        self, organization_id: uuid.UUID, *, actor_id: uuid.UUID | None = None
    ) -> OrganizationModel: ...

    @abstractmethod
    async def get_by_enter_token(
        self,
        enter_token: str,
    ) -> OrganizationModel: ...
