from typing import TYPE_CHECKING, NotRequired, TypedDict

import msgspec

from app.core.models import EntityDto


if TYPE_CHECKING:
    from app.core.models import UserModel


class UsersGetParams(TypedDict):
    user__normal_email: NotRequired[str | None]


class UserReadDto(EntityDto, frozen=True):
    name: str
    email: str

    @classmethod
    def from_user(cls, user: UserModel) -> UserReadDto:
        return cls(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_removed=user.is_removed,
            name=user.name,
            email=user.email,
        )


class UserSignUpDto(msgspec.Struct, frozen=True):
    name: str
    email: str
    password: str


class UserSignInDto(msgspec.Struct, frozen=True):
    login: str
    password: str


class UserUpdateDto(msgspec.Struct, frozen=True):
    name: str


class UserEmailDto(msgspec.Struct, frozen=True):
    email: str


class UserPasswordRecovery(msgspec.Struct, frozen=True):
    token: str
    new_password: str


class UserTokensDto(msgspec.Struct, frozen=True):
    access: str
    refresh: str
