import enum
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any, ClassVar

from jose import JWTError, jwt

from app.core.application.interfaces.services.tokens import ITokensService
from app.core.config import env_config
from app.core.exceptions.auth import UnauthorizedError


class TokenType(enum.StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
    EXPIRE = "EXPIRE"


class JwtService(ITokensService):
    ALGORITHM: ClassVar[str] = "HS256"
    TIME_DELTA_ACCESS: ClassVar[timedelta] = timedelta(minutes=env_config.access_token_minutes)
    TIME_DELTA_REFRESH: ClassVar[timedelta] = timedelta(days=env_config.refresh_token_days)

    def generate_access_token(self, user_id: uuid.UUID) -> str:
        return jwt.encode(
            {
                "token_type": TokenType.ACCESS,
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
                "exp": datetime.now(tz=UTC) + expiration,
                "iat": datetime.now(tz=UTC),
                "sub": str(user_id),
                "data": data,
            },
            key=env_config.secret_key,
            algorithm=self.ALGORITHM,
        )

    def identify_access_token(self, token: str) -> uuid.UUID:
        payload = self._identify_token(token, TokenType.ACCESS)
        return uuid.UUID(payload["sub"])

    def identify_refresh_token(self, token: str) -> uuid.UUID:
        payload = self._identify_token(token, TokenType.REFRESH)
        return uuid.UUID(payload["sub"])

    def identify_expire_token(self, token: str) -> tuple[uuid.UUID, dict[str, str] | None]:
        payload = self._identify_token(token, TokenType.EXPIRE)

        payload_data: dict[str, str] | None = None

        if "data" in payload and isinstance(payload["data"], dict):
            payload_data = payload["data"]

        return uuid.UUID(payload["sub"]), payload_data

    def _identify_token(self, token: str, type_: TokenType) -> dict[str, str]:
        try:
            payload = jwt.decode(token=token, key=env_config.secret_key, algorithms=[self.ALGORITHM])
            self._verify_token_payload(payload, type_)
        except (ValueError, KeyError, JWTError) as e:
            raise UnauthorizedError("Невалидный токен") from e
        else:
            return payload

    def _verify_token_payload(self, payload: dict[str, Any], type_: TokenType) -> dict[str, Any]:
        if payload["token_type"] != type_ or not payload["sub"]:
            raise ValueError("Невалидный токен")
        return payload
