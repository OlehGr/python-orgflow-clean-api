import enum
import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.exceptions.permission import PermissionDeniedError
from app.core.models.base import EntityDto, EntityModel
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
        role: OrganizationMemberRole = OrganizationMemberRole.MEMBER,
    ) -> "OrganizationMemberModel":
        return cls(**cls._generate_base_args(), user_id=user_id, organization_id=organization_id, role=role)

    def set_role(self, role: OrganizationMemberRole) -> None:
        self.role = role

    def ensure_permission(self, permission: Permission) -> None:
        current_permissions = ROLE_PERMISSIONS[self.role]

        if Permission.ALL in current_permissions:
            return

        if permission not in current_permissions:
            raise PermissionDeniedError(f"Доступ к {permission} запрещен")

    def to_entity_subject_event(
        self, subject: EntityEventSubject, *, producer_id: uuid.UUID | None
    ) -> EntityEvent["OrganizationMemberEventDto"]:
        return EntityEvent(
            producer_id=producer_id,
            subject=subject,
            entity=EntityEventEntity.organization_member,
            entity_id=self.id,
            data=OrganizationMemberEventDto.from_organization_member(self),
        )

    def to_entity_save_event(self, *, producer_id: uuid.UUID | None) -> EntityEvent["OrganizationMemberEventDto"]:
        return self.to_entity_subject_event(
            self._resolve_entity_save_subject(
                EntityEventSubject.organization_member_create,
                EntityEventSubject.organization_member_update,
            ),
            producer_id=producer_id,
        )

    def to_entity_delete_event(self, *, producer_id: uuid.UUID | None) -> EntityEvent["OrganizationMemberEventDto"]:
        return self.to_entity_subject_event(EntityEventSubject.organization_member_delete, producer_id=producer_id)


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
