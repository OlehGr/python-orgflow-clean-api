import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import get_b64encode_token
from app.core.models.entity import EntityDto, EntityModel
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject


class OrganizationModel(EntityModel):
    __tablename__ = "organization"

    name: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)

    enter_token: Mapped[str] = mapped_column(unique=True, index=True)

    @classmethod
    def create(cls, *, name: str, actor_id: uuid.UUID) -> "OrganizationModel":
        entity = cls(**cls._generate_base_args(), name=name, author_id=actor_id, enter_token=get_b64encode_token())
        entity.add_events(entity.to_entity_subject_event(EntityEventSubject.organization_create, actor_id=actor_id))
        return entity

    def update(self, *, name: str, actor_id: uuid.UUID | None) -> None:
        self.name = name
        self.add_events(self.to_entity_subject_event(EntityEventSubject.organization_update, actor_id=actor_id))

    def reset_enter_token(self, *, actor_id: uuid.UUID | None) -> None:
        self.enter_token = get_b64encode_token()
        self.add_events(self.to_entity_subject_event(EntityEventSubject.organization_update, actor_id=actor_id))

    def delete(self, *, actor_id: uuid.UUID | None) -> None:
        self.add_events(self.to_entity_subject_event(EntityEventSubject.organization_delete, actor_id=actor_id))

    def to_entity_subject_event(
        self, subject: EntityEventSubject, *, actor_id: uuid.UUID | None
    ) -> EntityEvent["OrganizationEventDto"]:
        return EntityEvent(
            producer_id=actor_id,
            subject=subject,
            entity=EntityEventEntity.organization,
            entity_id=self.id,
            data=OrganizationEventDto.from_organization(self),
        )


class OrganizationEventDto(EntityDto, frozen=True):
    name: str
    author_id: uuid.UUID
    enter_token: str

    @classmethod
    def from_organization(cls, organization: OrganizationModel) -> "OrganizationEventDto":
        return cls(
            id=organization.id,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
            is_removed=organization.is_removed,
            name=organization.name,
            author_id=organization.author_id,
            enter_token=organization.enter_token,
        )
