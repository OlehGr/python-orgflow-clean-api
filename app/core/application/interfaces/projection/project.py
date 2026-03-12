import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.project import ProjectReadDto, ProjectsWithLimitationGetParams


class IProjectProjection(Protocol):
    @abstractmethod
    async def get_by_id(self, project_id: uuid.UUID, *, actor_id: uuid.UUID | None) -> ProjectReadDto: ...

    @abstractmethod
    async def get_paged(
        self, *, actor_id: uuid.UUID, **kwargs: Unpack[ProjectsWithLimitationGetParams]
    ) -> Paged[ProjectReadDto]: ...

    @abstractmethod
    async def get_paginated(
        self, *, actor_id: uuid.UUID, **kwargs: Unpack[ProjectsWithLimitationGetParams]
    ) -> Paginated[ProjectReadDto]: ...
