from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    import uuid
    from datetime import timedelta


class IJwtService(Protocol):
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
    def verify_access_token(self, token: str, user_id: uuid.UUID) -> None: ...

    @abstractmethod
    def verify_refresh_token(self, token: str, user_id: uuid.UUID) -> None: ...

    @abstractmethod
    def verify_expire_token(
        self,
        token: str,
        user_id: uuid.UUID,
    ) -> dict[str, str] | None: ...
