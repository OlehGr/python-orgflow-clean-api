from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import EntityModel


class UserModel(EntityModel):
    __tablename__ = "user"

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_confirmed: Mapped[bool]
    is_active: Mapped[bool]

    @classmethod
    def create(
        cls,
        *,
        name: str,
        email: str,
        is_confirmed: bool = True,
    ) -> UserModel:
        return cls(
            *cls._generate_base_args(),
            name=name,
            email=email,
            is_confirmed=is_confirmed,
            is_active=True,
        )
