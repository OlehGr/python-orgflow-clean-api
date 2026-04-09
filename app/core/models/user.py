import uuid

import bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.exceptions.validation import ConflictError
from app.core.models.entity import EntityDto, EntityModel
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject


class UserModel(EntityModel):
    __tablename__ = "user"

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_confirmed: Mapped[bool]
    is_active: Mapped[bool]
    password_hash: Mapped[str]

    avatar_file_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("file.id", ondelete="SET NULL"), nullable=True, index=True
    )

    @classmethod
    def create(cls, *, name: str, email: str, password: str) -> "UserModel":
        password_hash = cls.hash_password(password)
        entity = cls(
            **cls._generate_base_args(),
            name=name,
            email=email,
            password_hash=password_hash,
            is_confirmed=False,
            is_active=True,
            avatar_file_id=None,
        )
        entity.add_events(entity.to_entity_subject_event(EntityEventSubject.user_create))
        return entity

    def update(self, *, name: str, actor_id: uuid.UUID | None = None) -> None:
        self.name = name
        self.add_events(self.to_entity_subject_event(EntityEventSubject.user_update, actor_id=actor_id))

    def confirm_user_email(self, email: str | None = None, *, actor_id: uuid.UUID | None = None) -> None:
        if not self.is_confirmed:
            self.is_confirmed = True

        if email:
            self.email = email

        self.add_events(self.to_entity_subject_event(EntityEventSubject.user_update, actor_id=actor_id))

    def verify_password(self, password: str) -> None:
        password_valid = bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

        if not password_valid:
            raise ConflictError("Неверный логин или пароль")

    def reset_password(self, new_password: str, *, actor_id: uuid.UUID | None = None) -> None:
        password_hash = self.hash_password(new_password)
        self.password_hash = password_hash
        self.add_events(self.to_entity_subject_event(EntityEventSubject.user_update, actor_id=actor_id))

    def delete(self, *, actor_id: uuid.UUID | None = None) -> None:
        self.add_events(self.to_entity_subject_event(EntityEventSubject.user_delete, actor_id=actor_id))

    @classmethod
    def hash_password(cls, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    @property
    def can_sign_in(self) -> bool:
        return self.is_active and self.is_confirmed

    @staticmethod
    def normalize_email(email: str) -> str:
        return email.lower()

    @staticmethod
    def validate_avatar_content_type(content_type: str) -> None:
        if not content_type.lower().startswith("image/"):
            raise ConflictError("Аватар пользователя должна быть картинка")

    def to_entity_subject_event(
        self, subject: EntityEventSubject, *, actor_id: uuid.UUID | None = None
    ) -> EntityEvent["UserEventDto"]:
        return EntityEvent(
            producer_id=actor_id,
            subject=subject,
            entity=EntityEventEntity.user,
            entity_id=self.id,
            data=UserEventDto.from_user(self),
        )


class UserEventDto(EntityDto, frozen=True):
    name: str
    email: str
    is_confirmed: bool
    is_active: bool
    password_hash: str
    avatar_file_id: uuid.UUID | None

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
            avatar_file_id=user.avatar_file_id,
        )
