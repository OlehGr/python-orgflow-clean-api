import bcrypt
from sqlalchemy.orm import Mapped, mapped_column

from app.core.exceptions.validation import InvalidCaseError
from app.core.models import EntityDto
from app.core.models.base import EntityModel


class UserModel(EntityModel):
    __tablename__ = "user"

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_confirmed: Mapped[bool]
    is_active: Mapped[bool]
    password_hash: Mapped[str]

    @classmethod
    def create(cls, *, name: str, email: str, password: str) -> "UserModel":
        password_hash = cls.hash_password(password)
        return cls(
            **cls._generate_base_args(),
            name=name,
            email=email,
            password_hash=password_hash,
            is_confirmed=False,
            is_active=True,
        )

    def update(self, *, name: str) -> None:
        self.name = name

    def confirm_user_email(self, email: str | None = None) -> None:
        self.is_confirmed = True

        if email:
            self.email = email

    def verify_password(self, password: str) -> None:
        password_valid = bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

        if not password_valid:
            raise InvalidCaseError("Неверный логин или пароль")

    def reset_password(self, new_password: str) -> None:
        password_hash = self.hash_password(new_password)
        self.password_hash = password_hash

    @classmethod
    def hash_password(cls, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    @property
    def can_sign_in(self) -> bool:
        return self.is_active and self.is_confirmed

    @classmethod
    def normalize_email(cls, email: str) -> str:
        return email.lower()


class UserEventDto(EntityDto, frozen=True):
    name: str
    email: str
    is_confirmed: bool
    is_active: bool
    password_hash: str

    @classmethod
    def from_user(cls, user: UserModel) -> "UserEventDto":
        return cls(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_removed=user.is_removed,
            is_active=user.is_active,
            is_confirmed=user.is_confirmed,
            password_hash=user.password_hash,
            name=user.name,
            email=user.email,
        )
