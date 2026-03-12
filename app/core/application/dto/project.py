import uuid
from typing import NotRequired, TypedDict

import msgspec

from app.core.application.dto.base import LimitationGetParams
from app.core.application.dto.organization import OrganizationReadDto
from app.core.application.dto.user import UserReadDto
from app.core.models import ProjectModel
from app.core.models.base import EntityDto


class ProjectsGetParams(TypedDict):
    project__id: NotRequired[set[uuid.UUID] | None]


class ProjectsWithLimitationGetParams(ProjectsGetParams, LimitationGetParams): ...


class ProjectReadDto(EntityDto, frozen=True):
    name: str
    organization_id: uuid.UUID
    organization: OrganizationReadDto
    author_id: uuid.UUID | None
    author: UserReadDto | None

    @classmethod
    def from_project(
        cls, project: ProjectModel, author: UserReadDto | None, organization: OrganizationReadDto
    ) -> "ProjectReadDto":
        return cls(
            id=project.id,
            created_at=project.created_at,
            updated_at=project.updated_at,
            is_removed=project.is_removed,
            name=project.name,
            author_id=project.author_id,
            organization_id=project.organization_id,
            author=author,
            organization=organization,
        )


class ProjectCreateDto(msgspec.Struct, frozen=True):
    name: str
    organization_id: uuid.UUID


class ProjectUpdateDto(msgspec.Struct, frozen=True):
    name: str
