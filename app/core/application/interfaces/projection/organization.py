import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.organization import (
    OrganizationReadDto,
    OrganizationSettingsReadDto,
    OrganizationsWithLimitationGetParams,
)


class IOrganizationProjection(Protocol):
    @abstractmethod
    async def get_by_id(self, organization_id: uuid.UUID, *, actor_id: uuid.UUID | None) -> OrganizationReadDto: ...

    @abstractmethod
    async def get_paged(
        self, *, actor_id: uuid.UUID, **kwargs: Unpack[OrganizationsWithLimitationGetParams]
    ) -> Paged[OrganizationReadDto]: ...

    @abstractmethod
    async def get_paginated(
        self, *, actor_id: uuid.UUID, **kwargs: Unpack[OrganizationsWithLimitationGetParams]
    ) -> Paginated[OrganizationReadDto]: ...


class IOrganizationSettingsProjection(Protocol):
    @abstractmethod
    async def get_by_id(
        self, organization_id: uuid.UUID, *, actor_id: uuid.UUID | None
    ) -> OrganizationSettingsReadDto: ...
