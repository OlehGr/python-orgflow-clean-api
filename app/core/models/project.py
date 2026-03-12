import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import EntityDto, EntityModel


class ProjectModel(EntityModel):
    __tablename__ = "project"

    name: Mapped[str]
    author_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), index=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), index=True)

    @classmethod
    def create(cls, *, name: str, organization_id: uuid.UUID, author_id: uuid.UUID) -> "ProjectModel":
        return cls(**cls._generate_base_args(), name=name, organization_id=organization_id, author_id=author_id)

    def update(self, *, name: str) -> None:
        self.name = name


class ProjectEventDto(EntityDto, frozen=True):
    name: str
    author_id: uuid.UUID | None

    @classmethod
    def from_project(cls, project: ProjectModel) -> "ProjectEventDto":
        return cls(
            id=project.id,
            created_at=project.created_at,
            updated_at=project.updated_at,
            is_removed=project.is_removed,
            name=project.name,
            author_id=project.author_id,
        )
