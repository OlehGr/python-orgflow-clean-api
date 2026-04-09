import enum
import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.exceptions.permission import PermissionDeniedError
from app.core.models.entity import EntityDto, EntityModel
from app.core.models.entity_event import EntityEvent, EntityEventEntity, EntityEventSubject
from app.core.models.permission import Permission


class OrganizationMemberRole(enum.StrEnum):
    MEMBER = "MEMBER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


ROLE_PERMISSIONS: dict[OrganizationMemberRole, set[Permission]] = {
    OrganizationMemberRole.ADMIN: {
        Permission.ALL,
    },
    OrganizationMemberRole.MANAGER: {Permission.PROJECT_CREATE, Permission.PROJECT_UPDATE, Permission.PROJECT_DELETE},
    OrganizationMemberRole.MEMBER: set(),
}


class OrganizationMemberModel(EntityModel):
    __tablename__ = "organization_member"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), index=True)
    role: Mapped[OrganizationMemberRole] = mapped_column(String())

    __table_args__ = (UniqueConstraint("user_id", "organization_id", name="uq_organization_member_user"),)

    @classmethod
    def create(
        cls,
        *,
        user_id: uuid.UUID,
        organization_id: uuid.UUID,
        actor_id: uuid.UUID | None,
        role: OrganizationMemberRole = OrganizationMemberRole.MEMBER,
    ) -> "OrganizationMemberModel":
        entity = cls(**cls._generate_base_args(), user_id=user_id, organization_id=organization_id, role=role)
        entity.add_events(
            entity.to_entity_subject_event(EntityEventSubject.organization_member_create, actor_id=actor_id)
        )
        return entity

    def set_role(self, role: OrganizationMemberRole, *, actor_id: uuid.UUID | None) -> None:
        self.role = role
        self.add_events(self.to_entity_subject_event(EntityEventSubject.organization_member_update, actor_id=actor_id))

    def ensure_permission(self, permission: Permission) -> None:
        current_permissions = ROLE_PERMISSIONS[self.role]

        if Permission.ALL in current_permissions:
            return

        if permission not in current_permissions:
            raise PermissionDeniedError(f"Доступ к {permission} запрещен")

    def delete(self, *, actor_id: uuid.UUID | None) -> None:
        self.add_events(self.to_entity_subject_event(EntityEventSubject.organization_member_delete, actor_id=actor_id))

    def to_entity_subject_event(
        self, subject: EntityEventSubject, *, actor_id: uuid.UUID | None
    ) -> EntityEvent["OrganizationMemberEventDto"]:
        return EntityEvent(
            producer_id=actor_id,
            subject=subject,
            entity=EntityEventEntity.organization_member,
            entity_id=self.id,
            data=OrganizationMemberEventDto.from_organization_member(self),
        )


class OrganizationMemberEventDto(EntityDto, frozen=True):
    organization_id: uuid.UUID
    user_id: uuid.UUID
    role: OrganizationMemberRole

    @classmethod
    def from_organization_member(cls, organization_member: OrganizationMemberModel) -> "OrganizationMemberEventDto":
        return cls(
            id=organization_member.id,
            created_at=organization_member.created_at,
            updated_at=organization_member.updated_at,
            is_removed=organization_member.is_removed,
            user_id=organization_member.user_id,
            organization_id=organization_member.organization_id,
            role=organization_member.role,
        )
