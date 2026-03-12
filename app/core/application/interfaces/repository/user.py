import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.user import UsersGetParams
from app.core.models.user import UserModel


class IUserRepository(Protocol):
    @abstractmethod
    async def save(self, user: UserModel) -> None: ...

    @abstractmethod
    async def delete(self, user: UserModel) -> None: ...

    @abstractmethod
    async def get_all(self, **kwargs: Unpack[UsersGetParams]) -> list[UserModel]: ...

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> UserModel: ...
