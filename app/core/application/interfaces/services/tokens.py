from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    import uuid
    from datetime import timedelta


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
