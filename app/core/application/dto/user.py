from typing import TYPE_CHECKING, NotRequired, TypedDict

from app.core.models import EntityDto


if TYPE_CHECKING:
    from app.core.models import UserModel


class UsersGetParams(TypedDict):
    user__email: NotRequired[str | None]


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
