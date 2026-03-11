from litestar import Router
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.exceptions.base import BasicMessageError
from app.presentation.shared.litestar.errors import internal_error_handler, message_error_handler
from .v1.auth import AuthController
from .v1.organization import OrganizationController
from .v1.organization_member import OrganizationMemberController
from .v1.user import UserController


app_api_router = Router(
    path="/api/v1",
    route_handlers=[AuthController, UserController, OrganizationController, OrganizationMemberController],
    exception_handlers={
        BasicMessageError: message_error_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_error_handler,
    },
)
