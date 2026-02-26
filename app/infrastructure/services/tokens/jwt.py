import enum
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, ClassVar

from jose import JWTError, jwt

from app.core.application.interfaces.services.jwt import IJwtService
from app.core.config import env_config
from app.core.exceptions.auth import UnauthorizedError


if TYPE_CHECKING:
    import uuid


class TokenType(enum.StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
    EXPIRE = "EXPIRE"


class JwtService(IJwtService):
    ALGORITHM: ClassVar[str] = "HS256"
    TIME_DELTA_ACCESS: ClassVar[timedelta] = timedelta(minutes=env_config.access_token_minutes)
    TIME_DELTA_REFRESH: ClassVar[timedelta] = timedelta(days=env_config.refresh_token_days)

    def generate_access_token(self, user_id: uuid.UUID) -> str:
        return jwt.encode(
            {
                "token_type": TokenType.ACCESS,
                "user_id": user_id,
                "exp": datetime.now(tz=UTC) + self.TIME_DELTA_ACCESS,
                "iat": datetime.now(tz=UTC),
                "sub": str(user_id),
            },
            key=env_config.secret_key,
            algorithm=self.ALGORITHM,
        )

    def generate_refresh_token(self, user_id: uuid.UUID) -> str:
        return jwt.encode(
            {
                "token_type": TokenType.REFRESH,
                "user_id": user_id,
                "exp": datetime.now(tz=UTC) + self.TIME_DELTA_REFRESH,
                "iat": datetime.now(tz=UTC),
                "sub": str(user_id),
            },
            key=env_config.secret_key,
            algorithm=self.ALGORITHM,
        )

    def generate_expire_token(
        self, user_id: uuid.UUID, expiration: timedelta, data: dict[str, str] | None = None
    ) -> str:
        return jwt.encode(
            {
                "token_type": TokenType.EXPIRE,
                "user_id": user_id,
                "exp": datetime.now(tz=UTC) + expiration,
                "iat": datetime.now(tz=UTC),
                "sub": str(user_id),
                "data": data,
            },
            key=env_config.secret_key,
            algorithm=self.ALGORITHM,
        )

    def verify_access_token(self, token: str, user_id: uuid.UUID) -> None:
        self._verify_token(token, user_id, TokenType.ACCESS)

    def verify_refresh_token(self, token: str, user_id: uuid.UUID) -> None:
        self._verify_token(token, user_id, TokenType.REFRESH)

    def verify_expire_token(self, token: str, user_id: uuid.UUID) -> dict[str, str] | None:
        payload = self._verify_token(token, user_id, TokenType.EXPIRE)

        if "data" not in payload or not isinstance(payload["data"], dict):
            raise UnauthorizedError("Невалидный токен")

        return payload["data"]

    def _verify_token(self, token: str, user_id: uuid.UUID, type_: TokenType) -> dict[str, str]:
        try:
            payload = jwt.decode(token=token, key=env_config.secret_key, algorithms=[self.ALGORITHM])
            self._verify_token_payload(payload, user_id, type_)
        except (ValueError, KeyError, JWTError) as e:
            raise UnauthorizedError("Невалидный токен") from e
        else:
            return payload

    def _verify_token_payload(self, payload: dict[str, Any], user_id: uuid.UUID, type_: TokenType) -> dict[str, Any]:
        if payload["token_type"] != type_ or payload["sub"] != str(user_id):
            raise ValueError("Невалидный токен")
        return payload
