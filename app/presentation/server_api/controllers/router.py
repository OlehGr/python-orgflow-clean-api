from litestar import Router

from app.presentation.shared.litestar.errors import internal_error_handler
from .v1.auth import AuthController
from .v1.user import UserController


app_api_router = Router(
    path="/api/v1",
    route_handlers=[AuthController, UserController],
    exception_handlers={Exception: internal_error_handler},
)
