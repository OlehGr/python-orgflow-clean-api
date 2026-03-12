import enum


class Permission(enum.StrEnum):
    ALL = "all:all"

    ORGANIZATION_UPDATE = "organization:update"
    ORGANIZATION_DELETE = "organization:delete"

    ORGANIZATION_MEMBER_CREATE = "organization_member:create"
    ORGANIZATION_MEMBER_UPDATE = "organization_member:update"
    ORGANIZATION_MEMBER_DELETE = "organization_member:delete"

    PROJECT_CREATE = "project:create"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
