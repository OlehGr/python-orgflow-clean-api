from collections.abc import Sequence

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, get, post, put
from litestar.status_codes import HTTP_200_OK

from app.core.application.dto.user import UserEmailDto, UserReadDto, UserUpdateDto
from app.core.application.interfaces.projection.user import IUserProjection
from app.core.application.services.user import UserService
from app.presentation.shared.schemas.base import MessageResultDto


class UserController(Controller):
    path = "/user"
    tags: Sequence[str] | None = ["User"]

    @post("/request-email-change", status_code=HTTP_200_OK)
    @inject
    async def request_email_change(
        self, user_service: FromDishka[UserService], request: Request, data: UserEmailDto
    ) -> MessageResultDto:
        await user_service.request_email_change(data, user_id=request.user)
        return MessageResultDto("Вам отправлено письмо с подтверждением")

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
