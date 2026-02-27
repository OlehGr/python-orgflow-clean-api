from collections.abc import Sequence

from dishka.integrations.litestar import FromDishka, inject
from litestar import Controller, Request, post
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.core.application.dto.user import (
    UserEmailDto,
    UserPasswordRecovery,
    UserRefreshTokenDto,
    UserSignInDto,
    UserSignUpDto,
    UserTokenDto,
    UserTokensDto,
)
from app.core.application.services.auth import AuthService
from app.core.application.services.user import UserService
from app.presentation.shared.schemas.base import MessageResultDto


class AuthController(Controller):
    path = "/auth"
    tags: Sequence[str] | None = ["Auth"]

    @post("/sign-up", status_code=HTTP_201_CREATED)
    @inject
    async def sign_up(self, user_service: FromDishka[UserService], data: UserSignUpDto) -> MessageResultDto:
        await user_service.sign_up_user(data)
        return MessageResultDto("Вам отправлено письмо с подтверждением")

    @post("/sign-in", status_code=HTTP_200_OK)
    @inject
    async def sign_in(self, user_service: FromDishka[UserService], data: UserSignInDto) -> UserTokensDto:
        return await user_service.sign_in_user(data)

    @post("/refresh", status_code=HTTP_200_OK)
    @inject
    async def refresh(self, auth_service: FromDishka[AuthService], data: UserRefreshTokenDto) -> UserTokensDto:
        return await auth_service.refresh_authorize(data.refresh)

    @post("/confirm", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def confirm(self, user_service: FromDishka[UserService], data: UserTokenDto) -> None:
        await user_service.confirm_user_email(data.token)

    @post("/request-password-recovery", status_code=HTTP_200_OK)
    @inject
    async def request_password_recovery(
        self, user_service: FromDishka[UserService], data: UserEmailDto
    ) -> MessageResultDto:
        await user_service.request_password_recovery(data)
        return MessageResultDto("Вам отправлена ссылка для восстановление пароля на почту")

    @post("/recovery-password", status_code=HTTP_200_OK)
    @inject
    async def recovery_password(
        self, user_service: FromDishka[UserService], data: UserPasswordRecovery
    ) -> MessageResultDto:
        await user_service.recovery_user_password(data)
        return MessageResultDto("Пароль успешно изменен")

    @post("/request-email-change", status_code=HTTP_200_OK)
    @inject
    async def request_email_change(
        self, user_service: FromDishka[UserService], request: Request, data: UserEmailDto
    ) -> MessageResultDto:
        await user_service.request_email_change(data, user_id=request.user)
        return MessageResultDto("Вам отправлено письмо с подтверждением")
