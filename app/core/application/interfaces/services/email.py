from abc import abstractmethod
from typing import Protocol


class IEmailService(Protocol):
    @abstractmethod
    async def send_confirmation_email(self, *, email: str, username: str, token: str) -> None: ...

    @abstractmethod
    async def send_recovery_email(self, *, email: str, username: str, token: str) -> None: ...
