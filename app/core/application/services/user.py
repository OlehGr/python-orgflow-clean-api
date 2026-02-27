import uuid
from dataclasses import dataclass
from datetime import timedelta

from app.core.application.dto.user import (
    UserEmailDto,
    UserPasswordRecovery,
    UserSignInDto,
    UserSignUpDto,
    UserTokensDto,
    UserUpdateDto,
)
from app.core.application.interfaces.common.background import IBackgroundExecutor
from app.core.application.interfaces.repository.user import IUserRepository
from app.core.application.interfaces.services.email import IEmailService
from app.core.application.interfaces.services.tokens import ITokensService
from app.core.exceptions.auth import UnauthorizedError
from app.core.exceptions.entity import EntityNotFoundError
from app.core.exceptions.validation import InvalidCaseError
from app.core.models import UserModel


@dataclass
class UserService:
    _user_repository: IUserRepository

    _tokens_service: ITokensService
    _email_service: IEmailService
    _background_executor: IBackgroundExecutor

    async def update_user(self, user_id: uuid.UUID, data: UserUpdateDto) -> uuid.UUID:
        user = await self._user_repository.get_by_id(user_id)
        user.update(name=data.name)
        await self._user_repository.save(user)
        return user.id

    async def sign_up_user(self, data: UserSignUpDto) -> uuid.UUID:
        normal_email = UserModel.normalize_email(data.email)

        email_users = await self._user_repository.get_all(user__normal_email=normal_email)

        if email_users:
            raise InvalidCaseError("Пользователь с таким Email уже существует")

        user = UserModel.create(name=data.name, email=normal_email, password=data.password)

        await self._user_repository.save(user)

        self._public_email_confirmation_for_user(user)

        return user.id

    async def sign_in_user(self, data: UserSignInDto) -> UserTokensDto:
        normal_email = UserModel.normalize_email(data.login)

        email_users = await self._user_repository.get_all(user__normal_email=normal_email)

        if not email_users:
            raise InvalidCaseError("Неверный логин или пароль")

        user = email_users[0]

        if not user.can_sign_in:
            raise InvalidCaseError("Необходимо подтвердить Email")

        user.verify_password(data.password)

        return self._generate_tokens_for_user(user)

    async def confirm_user_email(self, token: str) -> None:
        user_id, data = self._tokens_service.identify_expire_token(token)

        try:
            user = await self._user_repository.get_by_id(user_id)
        except EntityNotFoundError as e:
            raise UnauthorizedError("Пользователь не найден") from e

        new_email = data.get("email", None) if data else None

        user.confirm_user_email(new_email)

        await self._user_repository.save(user)

    async def request_email_change(self, data: UserEmailDto, *, user_id: uuid.UUID) -> None:
        user = await self._user_repository.get_by_id(user_id)
        email = UserModel.normalize_email(data.email)

        if not user.is_confirmed:
            raise InvalidCaseError("Чтобы изменять email необходимо подтвердить аккаунт")

        if user.email == email:
            raise InvalidCaseError("Email не отличается от текущего")

        expire_token = self._tokens_service.generate_expire_token(
            user_id=user.id, expiration=timedelta(minutes=15), data={"email": email}
        )

        await self._email_service.send_confirmation_email(email=email, username=user.name, token=expire_token)

    async def request_password_recovery(self, data: UserEmailDto) -> None:
        email_users = await self._user_repository.get_all(user__normal_email=UserModel.normalize_email(data.email))

        if not email_users:
            raise UnauthorizedError("Пользователя с таким Email не существует")

        user = email_users[0]

        expire_token = self._tokens_service.generate_expire_token(user_id=user.id, expiration=timedelta(minutes=15))

        await self._email_service.send_recovery_email(email=user.email, username=user.name, token=expire_token)

    async def recovery_user_password(self, data: UserPasswordRecovery) -> None:
        user_id, _ = self._tokens_service.identify_expire_token(data.token)

        try:
            user = await self._user_repository.get_by_id(user_id)
        except EntityNotFoundError as e:
            raise UnauthorizedError("Пользователь не найден") from e

        user.reset_password(data.new_password)
        user.confirm_user_email()

        await self._user_repository.save(user)

    def _generate_tokens_for_user(self, user: UserModel) -> UserTokensDto:
        access = self._tokens_service.generate_access_token(user.id)
        refresh = self._tokens_service.generate_refresh_token(user.id)

        return UserTokensDto(access=access, refresh=refresh)

    def _public_email_confirmation_for_user(self, user: UserModel) -> None:
        expire_token = self._tokens_service.generate_expire_token(user.id, timedelta(days=356))

        self._background_executor.submit(
            self._email_service.send_confirmation_email(email=user.email, username=user.name, token=expire_token)
        )
