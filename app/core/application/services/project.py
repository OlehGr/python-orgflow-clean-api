import uuid
from dataclasses import dataclass

from app.core.application.dto.project import ProjectCreateDto, ProjectUpdateDto
from app.core.application.interfaces.repository.project import IProjectRepository
from app.core.models import ProjectModel


@dataclass
class ProjectService:
    _project_repository: IProjectRepository

    async def create_project(self, data: ProjectCreateDto, *, actor_id: uuid.UUID) -> uuid.UUID:
        project = ProjectModel.create(name=data.name, organization_id=data.organization_id, author_id=actor_id)

        await self._project_repository.save(project, actor_id=actor_id)

        return project.id

    async def update_project(self, project_id: uuid.UUID, data: ProjectUpdateDto, *, actor_id: uuid.UUID) -> None:
        project = await self._project_repository.get_by_id(project_id, actor_id=actor_id)

        project.update(name=data.name)

        await self._project_repository.save(project, actor_id=actor_id)

    async def delete_project(self, project_id: uuid.UUID, *, actor_id: uuid.UUID) -> None:
        project = await self._project_repository.get_by_id(project_id, actor_id=actor_id)

        await self._project_repository.delete(project, actor_id=actor_id)
