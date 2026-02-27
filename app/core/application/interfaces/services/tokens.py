import uuid
from abc import abstractmethod
from datetime import timedelta
from typing import Protocol


class ITokensService(Protocol):
    @abstractmethod
    def generate_access_token(self, user_id: uuid.UUID) -> str: ...

    @abstractmethod
    def generate_refresh_token(self, user_id: uuid.UUID) -> str: ...

    @abstractmethod
    def generate_expire_token(
        self,
        user_id: uuid.UUID,
        expiration: timedelta,
        data: dict[str, str] | None = None,
    ) -> str: ...

    @abstractmethod
    def identify_access_token(self, token: str) -> uuid.UUID: ...

    @abstractmethod
    def identify_refresh_token(self, token: str) -> uuid.UUID: ...

    @abstractmethod
    def identify_expire_token(
        self,
        token: str,
    ) -> tuple[uuid.UUID, dict[str, str] | None]: ...
