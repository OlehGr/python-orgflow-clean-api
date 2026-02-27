from app.core.application.services.auth import AuthService
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, DefineMiddleware
from litestar.middleware.authentication import AuthenticationResult


class _TokenMiddlewareAuthentication(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self,
        connection: ASGIConnection,
    ) -> AuthenticationResult:
        auth_header = connection.headers.get("Authorization")
        if not auth_header:
            msg = "No JWT token found in request header"
            raise NotAuthorizedException(msg)

        encoded_token = auth_header.partition(" ")[-1]

        auth_service: AuthService = connection.app.state.auth_service

        user_id = await auth_service.authorize(encoded_token)

        return AuthenticationResult(user=user_id, auth=encoded_token)


token_auth_middleware = DefineMiddleware(
    _TokenMiddlewareAuthentication,
    exclude=[
        "docs",
        "/v1/external",
        "/v1/auth/sign-in",
        "/v1/auth/sign-up",
        "/v1/auth/confirm",
        "/v1/auth/refresh",
        "/v1/auth/recovery-password",
        "/v1/auth/request-password-recovery",
    ],
)
