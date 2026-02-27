import uuid
from abc import abstractmethod
from typing import Protocol, Unpack

from app.core.application.dto.base import Paged, Paginated
from app.core.application.dto.user import UserReadDto, UsersGetParams


class IUserProjection(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> UserReadDto: ...

    @abstractmethod
    async def get_paged(self, **kwargs: Unpack[UsersGetParams]) -> Paged[UserReadDto]: ...

    @abstractmethod
    async def get_paginated(self, **kwargs: Unpack[UsersGetParams]) -> Paginated[UserReadDto]: ...
