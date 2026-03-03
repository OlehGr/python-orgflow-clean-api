from typing import NotRequired, Optional, TypedDict

import msgspec

from app.core.models import EntityDto, FileModel, UserModel


class UsersGetParams(TypedDict):
    user__normal_email: NotRequired[str | None]


class UserReadDto(EntityDto, frozen=True):
    name: str
    email: str
    avatar: Optional["UserAvatarReadDto"]

    @classmethod
    def from_user(cls, user: UserModel, avatar: Optional["UserAvatarReadDto"]) -> "UserReadDto":
        return cls(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_removed=user.is_removed,
            name=user.name,
            email=user.email,
            avatar=avatar,
        )


class UserAvatarReadDto(EntityDto, frozen=True):
    url: str

    @classmethod
    def from_file(cls, file: FileModel) -> "UserAvatarReadDto":
        return cls(
            id=file.id, created_at=file.created_at, updated_at=file.updated_at, is_removed=file.is_removed, url=file.url
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


class UserRefreshTokenDto(msgspec.Struct, frozen=True):
    refresh: str


class UserTokenDto(msgspec.Struct, frozen=True):
    token: str
