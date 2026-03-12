import uuid
from collections.abc import Sequence

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, delete, get, post
from litestar.handlers import put
from litestar.params import Parameter
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.project import ProjectCreateDto, ProjectReadDto, ProjectUpdateDto
from app.core.application.interfaces.projection.project import IProjectProjection
from app.core.application.services.project import ProjectService


class ProjectController(Controller):
    path = "/project"
    tags: Sequence[str] | None = ["Project"]

    @get(status_code=HTTP_200_OK)
    @inject
    async def get_paged(
        self,
        project_projection: FromDishka[IProjectProjection],
        request: Request,
        page: int = Parameter(default=1, required=False),
        limit: int = Parameter(default=50, required=False),
        project__id: set[uuid.UUID] | None = Parameter(default=None, required=False),
    ) -> Paged[ProjectReadDto]:
        return await project_projection.get_paged(
            actor_id=request.user, page=page, limit=limit, project__id=project__id
        )

    @get("/paginated", status_code=HTTP_200_OK)
    @inject
    async def get_paginated(
        self,
        project_projection: FromDishka[IProjectProjection],
        request: Request,
        page: int = Parameter(default=1, required=False),
        limit: int = Parameter(default=50, required=False),
        project__id: set[uuid.UUID] | None = Parameter(default=None, required=False),
    ) -> Paginated[ProjectReadDto]:
        return await project_projection.get_paginated(
            actor_id=request.user, page=page, limit=limit, project__id=project__id
        )

    @post(status_code=HTTP_201_CREATED)
    @inject
    async def create(
        self,
        project_projection: FromDishka[IProjectProjection],
        project_service: FromDishka[ProjectService],
        request: Request,
        data: ProjectCreateDto,
    ) -> ProjectReadDto:
        project_id = await project_service.create_project(data, actor_id=request.user)
        return await project_projection.get_by_id(project_id, actor_id=None)

    @put("/{project_id:uuid}", status_code=HTTP_200_OK)
    @inject
    async def update(
        self,
        project_projection: FromDishka[IProjectProjection],
        project_service: FromDishka[ProjectService],
        request: Request,
        project_id: uuid.UUID,
        data: ProjectUpdateDto,
    ) -> ProjectReadDto:
        await project_service.update_project(project_id, data, actor_id=request.user)
        return await project_projection.get_by_id(project_id, actor_id=None)

    @delete("/{project_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def delete(
        self,
        project_service: FromDishka[ProjectService],
        request: Request,
        project_id: uuid.UUID,
    ) -> None:
        await project_service.delete_project(project_id, actor_id=request.user)

    @get("/{project_id:uuid}", status_code=HTTP_200_OK)
    @inject
    async def get_by_id(
        self,
        project_projection: FromDishka[IProjectProjection],
        request: Request,
        project_id: uuid.UUID,
    ) -> ProjectReadDto:
        return await project_projection.get_by_id(project_id, actor_id=request.user)
