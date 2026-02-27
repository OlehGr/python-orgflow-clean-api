import uuid
from dataclasses import dataclass

from app.core.application.dto.user import UserTokensDto
from app.core.application.interfaces.repository.user import IUserRepository
from app.core.application.interfaces.services.tokens import ITokensService
from app.core.exceptions.auth import UnauthorizedError
from app.core.exceptions.entity import EntityNotFoundError


@dataclass
class AuthService:
    _user_repository: IUserRepository

    _tokens_service: ITokensService

    async def refresh_authorize(self, refresh_token: str) -> UserTokensDto:
        user_id = self._tokens_service.identify_refresh_token(refresh_token)

        try:
            user = await self._user_repository.get_by_id(user_id)
        except EntityNotFoundError as e:
            raise UnauthorizedError("Пользователь не найден") from e

        access_token = self._tokens_service.generate_access_token(user.id)

        return UserTokensDto(access=access_token, refresh=refresh_token)

    async def authorize(self, access_token: str) -> uuid.UUID:
        return self._tokens_service.identify_access_token(access_token)
