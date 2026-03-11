import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import EntityDto, EntityModel


class OrganizationModel(EntityModel):
    __tablename__ = "organization"

    name: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)

    @classmethod
    def create(cls, *, name: str, author_id: uuid.UUID) -> "OrganizationModel":
        return cls(**cls._generate_base_args(), name=name, author_id=author_id)

    def update(self, *, name: str) -> None:
        self.name = name


class OrganizationEventDto(EntityDto, frozen=True):
    name: str
    author_id: uuid.UUID

    @classmethod
    def from_organization(cls, organization: OrganizationModel) -> "OrganizationEventDto":
        return cls(
            id=organization.id,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
            is_removed=organization.is_removed,
            name=organization.name,
            author_id=organization.author_id,
        )
