from collections.abc import Sequence

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, get, put
from litestar.status_codes import HTTP_200_OK

from app.core.application.dto.user import UserReadDto, UserUpdateDto
from app.core.application.interfaces.projection.user import IUserProjection
from app.core.application.services.user import UserService


class UserController(Controller):
    path = "/user"
    tags: Sequence[str] | None = ["User"]

    @get("/me", status_code=HTTP_200_OK)
    @inject
    async def get_me(self, user_projection: FromDishka[IUserProjection], request: Request) -> UserReadDto:
        return await user_projection.get_by_id(request.user)

    @put("/me", status_code=HTTP_200_OK)
    @inject
    async def update_me(
        self,
        user_service: FromDishka[UserService],
        user_projection: FromDishka[IUserProjection],
        request: Request,
        data: UserUpdateDto,
    ) -> UserReadDto:
        user_id = await user_service.update_user(request.user, data)
        return await user_projection.get_by_id(user_id)
