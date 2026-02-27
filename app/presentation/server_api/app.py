from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from dishka import AsyncContainer
from dishka.integrations.litestar import (
    setup_dishka as setup_litestar_dishka,
)
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.openapi.spec import Components, SecurityScheme
from litestar.plugins.structlog import StructlogConfig, StructlogPlugin

from app.core.config import env_config
from app.presentation.shared.litestar.middlewares.auth import token_auth_middleware
from .controllers.router import app_api_router


def create_litestar_app(
    container: AsyncContainer, lifespan: Callable[[Litestar], AbstractAsyncContextManager]
) -> Litestar:
    app = Litestar(
        route_handlers=[app_api_router],
        request_max_body_size=1024 * 1024 * 1024,
        cors_config=CORSConfig(allow_origins=["*"]),
        openapi_config=OpenAPIConfig(
            title="Some Api",
            version="1.0.0",
            path="/api/docs",
            render_plugins=[SwaggerRenderPlugin()],
            security=[{"BearerToken": []}],
            components=Components(
                security_schemes={
                    "BearerToken": SecurityScheme(
                        type="http",
                        scheme="bearer",
                    )
                },
            ),
        ),
        plugins=[
            StructlogPlugin(
                config=StructlogConfig(
                    middleware_logging_config=LoggingMiddlewareConfig(
                        response_log_fields=["status_code", "cookies", "headers"]
                    )
                )
            )
        ],
        middleware=[token_auth_middleware],
        lifespan=[lifespan],
        debug=env_config.debug,
    )
    setup_litestar_dishka(container, app)
    return app
