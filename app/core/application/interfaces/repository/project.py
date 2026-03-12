import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.project import ProjectsGetParams
from app.core.models import ProjectModel


class IProjectRepository(Protocol):
    @abstractmethod
    async def save(self, project: ProjectModel, *, actor_id: uuid.UUID | None) -> None: ...

    @abstractmethod
    async def delete(self, project: ProjectModel, *, actor_id: uuid.UUID | None) -> None: ...

    @abstractmethod
    async def get_all(
        self, *, actor_id: uuid.UUID | None = None, **kwargs: Unpack[ProjectsGetParams]
    ) -> list[ProjectModel]: ...

    @abstractmethod
    async def get_by_id(self, project_id: uuid.UUID, *, actor_id: uuid.UUID | None = None) -> ProjectModel: ...
