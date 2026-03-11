import enum
import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import EntityDto, EntityModel


class OrganizationMemberRole(enum.StrEnum):
    MEMBER = "MEMBER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


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
