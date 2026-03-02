from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from litestar import Litestar

from app.core.application.services.auth import AuthService
from app.core.application.services.entity_event import EntityEventService
from app.infrastructure.database.providers import DatabaseInjectionsProvider
from app.presentation.server_api.app import create_litestar_app
from .providers import AppInjectionsProvider


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncIterator[None]:
    container: AsyncContainer = app.state.dishka_container

    await container.get(EntityEventService)

    try:
        app.state.auth_service = await container.get(AuthService)
        yield
    finally:
        await container.close()


container = make_async_container(DatabaseInjectionsProvider(), AppInjectionsProvider())

app = create_litestar_app(container, lifespan)
