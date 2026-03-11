import uuid
from collections.abc import Sequence

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, delete, get, post, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.organization_member import (
    OrganizationMemberCreateDto,
    OrganizationMemberReadDto,
    OrganizationMemberUpdateRoleDto,
)
from app.core.application.interfaces.projection.organization_member import IOrganizationMemberProjection
from app.core.application.services.orgnaization import OrganizationMemberService


class OrganizationMemberController(Controller):
    path = "/organization_member"
    tags: Sequence[str] | None = ["OrganizationMember"]

    @get(status_code=HTTP_200_OK)
    @inject
    async def get_paged(
        self,
        organization_member_projection: FromDishka[IOrganizationMemberProjection],
        request: Request,
        page: int = Parameter(default=1, required=False),
        limit: int = Parameter(default=50, required=False),
        organization_member__organization_id: uuid.UUID | None = Parameter(default=None, required=False),
        organization_member__user_id: uuid.UUID | None = Parameter(default=None, required=False),
    ) -> Paged[OrganizationMemberReadDto]:
        return await organization_member_projection.get_paged(
            actor_id=request.user,
            page=page,
            limit=limit,
            organization_member__organization_id=organization_member__organization_id,
            organization_member__user_id=organization_member__user_id,
        )

    @get("/paginated", status_code=HTTP_200_OK)
    @inject
    async def get_paginated(
        self,
        organization_member_projection: FromDishka[IOrganizationMemberProjection],
        request: Request,
        page: int = Parameter(default=1, required=False),
        limit: int = Parameter(default=50, required=False),
        organization_member__organization_id: uuid.UUID | None = Parameter(default=None, required=False),
        organization_member__user_id: uuid.UUID | None = Parameter(default=None, required=False),
    ) -> Paginated[OrganizationMemberReadDto]:
        return await organization_member_projection.get_paginated(
            actor_id=request.user,
            page=page,
            limit=limit,
            organization_member__organization_id=organization_member__organization_id,
            organization_member__user_id=organization_member__user_id,
        )

    @post(status_code=HTTP_201_CREATED)
    @inject
    async def create(
        self,
        organization_member_projection: FromDishka[IOrganizationMemberProjection],
        organization_member_service: FromDishka[OrganizationMemberService],
        request: Request,
        data: OrganizationMemberCreateDto,
    ) -> OrganizationMemberReadDto:
        organization_member_id = await organization_member_service.create_organization_member(
            data, actor_id=request.user
        )
        return await organization_member_projection.get_by_id(organization_member_id, actor_id=None)

    @put("/{organization_member_id:uuid}/role", status_code=HTTP_200_OK)
    @inject
    async def update_role(
        self,
        organization_member_projection: FromDishka[IOrganizationMemberProjection],
        organization_member_service: FromDishka[OrganizationMemberService],
        request: Request,
        organization_member_id: uuid.UUID,
        data: OrganizationMemberUpdateRoleDto,
    ) -> OrganizationMemberReadDto:
        await organization_member_service.update_organization_member_role(
            organization_member_id, data, actor_id=request.user
        )
        return await organization_member_projection.get_by_id(organization_member_id, actor_id=None)

    @delete("/{organization_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def delete(
        self,
        organization_member_service: FromDishka[OrganizationMemberService],
        request: Request,
        organization_id: uuid.UUID,
    ) -> None:
        await organization_member_service.delete_organization_member(organization_id, actor_id=request.user)

    @get("/{organization_id:uuid}", status_code=HTTP_200_OK)
    @inject
    async def get_by_id(
        self,
        organization_member_projection: FromDishka[IOrganizationMemberProjection],
        request: Request,
        organization_id: uuid.UUID,
    ) -> OrganizationMemberReadDto:
        return await organization_member_projection.get_by_id(organization_id, actor_id=request.user)
