import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import EntityDto, EntityModel, get_b64encode_token
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject


class OrganizationModel(EntityModel):
    __tablename__ = "organization"

    name: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)

    enter_token: Mapped[str] = mapped_column(unique=True, index=True)

    @classmethod
    def create(cls, *, name: str, author_id: uuid.UUID) -> "OrganizationModel":
        return cls(**cls._generate_base_args(), name=name, author_id=author_id, enter_token=get_b64encode_token())

    def update(self, *, name: str) -> None:
        self.name = name

    def reset_enter_token(self) -> None:
        self.enter_token = get_b64encode_token()

    def to_entity_subject_event(
        self, subject: EntityEventSubject, *, producer_id: uuid.UUID | None
    ) -> EntityEvent["OrganizationEventDto"]:
        return EntityEvent(
            producer_id=producer_id,
            subject=subject,
            entity=EntityEventEntity.organization,
            entity_id=self.id,
            data=OrganizationEventDto.from_organization(self),
        )

    def to_entity_save_event(self, *, producer_id: uuid.UUID | None) -> EntityEvent["OrganizationEventDto"]:
        return self.to_entity_subject_event(
            self._resolve_entity_save_subject(
                EntityEventSubject.organization_create, EntityEventSubject.organization_update
            ),
            producer_id=producer_id,
        )

    def to_entity_delete_event(self, *, producer_id: uuid.UUID | None) -> EntityEvent["OrganizationEventDto"]:
        return self.to_entity_subject_event(EntityEventSubject.organization_delete, producer_id=producer_id)


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
