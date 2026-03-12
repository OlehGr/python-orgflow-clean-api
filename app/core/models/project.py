import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import EntityDto, EntityModel
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject


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

    def to_entity_subject_event(
        self, subject: EntityEventSubject, *, producer_id: uuid.UUID | None
    ) -> EntityEvent["ProjectEventDto"]:
        return EntityEvent(
            producer_id=producer_id,
            subject=subject,
            entity=EntityEventEntity.project,
            entity_id=self.id,
            data=ProjectEventDto.from_project(self),
        )

    def to_entity_save_event(self, *, producer_id: uuid.UUID | None) -> EntityEvent["ProjectEventDto"]:
        return self.to_entity_subject_event(
            self._resolve_entity_save_subject(EntityEventSubject.project_create, EntityEventSubject.project_update),
            producer_id=producer_id,
        )

    def to_entity_delete_event(self, *, producer_id: uuid.UUID | None) -> EntityEvent["ProjectEventDto"]:
        return self.to_entity_subject_event(EntityEventSubject.project_delete, producer_id=producer_id)


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
