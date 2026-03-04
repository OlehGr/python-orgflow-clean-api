from collections.abc import Sequence

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, get, post, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_200_OK

from app.core.application.dto.file import FileCreateStreamData
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
        user_id = request.user
        await user_service.update_user(user_id, data)
        return await user_projection.get_by_id(user_id)

    @put(
        "/me/avatar",
        status_code=HTTP_200_OK,
    )
    @inject
    async def update_me_avatar(
        self,
        user_service: FromDishka[UserService],
        user_projection: FromDishka[IUserProjection],
        request: Request,
        filename: str = Parameter(required=True),
    ) -> UserReadDto:
        content_type = request.headers.get("content-type", "application/octet-stream")

        user_id = request.user
        await user_service.update_user_avatar(
            user_id,
            FileCreateStreamData(
                name=filename,
                content_type=content_type,
                file_stream=request.stream(),
            ),
        )
        return await user_projection.get_by_id(user_id)
