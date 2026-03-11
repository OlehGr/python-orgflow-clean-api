import uuid
from collections.abc import Sequence

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, delete, get, post
from litestar.handlers import put
from litestar.params import Parameter
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.organization import OrganizationCreateDto, OrganizationReadDto, OrganizationUpdateDto
from app.core.application.interfaces.projection.organization import IOrganizationProjection
from app.core.application.services.orgnaization import OrganizationService


class OrganizationController(Controller):
    path = "/organization"
    tags: Sequence[str] | None = ["Organization"]

    @get(status_code=HTTP_200_OK)
    @inject
    async def get_paged(
        self,
        organization_projection: FromDishka[IOrganizationProjection],
        request: Request,
        page: int = Parameter(default=1, required=False),
        limit: int = Parameter(default=50, required=False),
        organization__id: set[uuid.UUID] | None = Parameter(default=None, required=False),
    ) -> Paged[OrganizationReadDto]:
        return await organization_projection.get_paged(
            actor_id=request.user, page=page, limit=limit, organization__id=organization__id
        )

    @get("/paginated", status_code=HTTP_200_OK)
    @inject
    async def get_paginated(
        self,
        organization_projection: FromDishka[IOrganizationProjection],
        request: Request,
        page: int = Parameter(default=1, required=False),
        limit: int = Parameter(default=50, required=False),
        organization__id: set[uuid.UUID] | None = Parameter(default=None, required=False),
    ) -> Paginated[OrganizationReadDto]:
        return await organization_projection.get_paginated(
            actor_id=request.user, page=page, limit=limit, organization__id=organization__id
        )

    @post(status_code=HTTP_201_CREATED)
    @inject
    async def create(
        self,
        organization_projection: FromDishka[IOrganizationProjection],
        organization_service: FromDishka[OrganizationService],
        request: Request,
        data: OrganizationCreateDto,
    ) -> OrganizationReadDto:
        organization_id = await organization_service.create_organization(data, actor_id=request.user)
        return await organization_projection.get_by_id(organization_id, actor_id=None)

    @put("/{organization_id:uuid}", status_code=HTTP_200_OK)
    @inject
    async def update(
        self,
        organization_projection: FromDishka[IOrganizationProjection],
        organization_service: FromDishka[OrganizationService],
        request: Request,
        organization_id: uuid.UUID,
        data: OrganizationUpdateDto,
    ) -> OrganizationReadDto:
        await organization_service.update_organization(organization_id, data, actor_id=request.user)
        return await organization_projection.get_by_id(organization_id, actor_id=None)

    @delete("/{organization_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def delete(
        self,
        organization_service: FromDishka[OrganizationService],
        request: Request,
        organization_id: uuid.UUID,
    ) -> None:
        await organization_service.delete_organization(organization_id, actor_id=request.user)

    @get("/{organization_id:uuid}", status_code=HTTP_200_OK)
    @inject
    async def get_by_id(
        self,
        organization_projection: FromDishka[IOrganizationProjection],
        request: Request,
        organization_id: uuid.UUID,
    ) -> OrganizationReadDto:
        return await organization_projection.get_by_id(organization_id, actor_id=request.user)
