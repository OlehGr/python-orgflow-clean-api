import uuid
from dataclasses import dataclass

from app.core.application.interfaces.repository.organization_member import IOrganizationMemberRepository
from app.core.exceptions.entity import EntityNotFoundError
from app.core.exceptions.permission import PermissionDeniedError
from app.core.models.permission import Permission


@dataclass
class PermissionService:
    _organization_member_repository: IOrganizationMemberRepository

    async def ensure(self, permission: Permission, *, actor_id: uuid.UUID | None, organization_id: uuid.UUID) -> None:
        if not actor_id:
            return

        try:
            organization_member = await self._organization_member_repository.get_user_organization_member(
                user_id=actor_id, organization_id=organization_id
            )
        except EntityNotFoundError as e:
            raise PermissionDeniedError(f"Доступ к {permission} запрещен") from e

        organization_member.ensure_permission(permission)
