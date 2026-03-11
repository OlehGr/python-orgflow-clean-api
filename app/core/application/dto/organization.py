import uuid
from typing import NotRequired, TypedDict

import msgspec

from app.core.application.dto.base import LimitationGetParams
from app.core.models import OrganizationModel
from app.core.models.base import EntityDto


class OrganizationsGetParams(TypedDict):
    organization__id: NotRequired[set[uuid.UUID] | None]


class OrganizationsWithLimitationGetParams(OrganizationsGetParams, LimitationGetParams): ...


class OrganizationReadDto(EntityDto, frozen=True):
    name: str
    author_id: uuid.UUID

    @classmethod
    def from_organization(cls, organization: OrganizationModel) -> "OrganizationReadDto":
        return cls(
            id=organization.id,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
            is_removed=organization.is_removed,
            name=organization.name,
            author_id=organization.author_id,
        )


class OrganizationCreateDto(msgspec.Struct, frozen=True):
    name: str


class OrganizationUpdateDto(msgspec.Struct, frozen=True):
    name: str
