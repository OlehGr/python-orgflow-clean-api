from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, Provider, make_async_container
from faststream.rabbit import RabbitBroker
from litestar import Litestar

from app.core.application.services.auth import AuthService
from app.core.application.services.entity_event import EntityEventService
from app.core.config.env import env_config
from app.infrastructure.database.providers import DatabaseInjectionsProvider
from app.infrastructure.rabbit.broker import RabbitInjectionsProvider
from app.presentation.app_api.app import create_litestar_app
from app.run.shared.providers import BaseRequiredInjectionsProvider
from .providers import AppInjectionsProvider, LocalMockInjectionsProvider


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncIterator[None]:
    container: AsyncContainer = app.state.dishka_container

    rabbit_broker = await container.get(RabbitBroker)
    await rabbit_broker.connect()

    await container.get(EntityEventService)

    try:
        app.state.auth_service = await container.get(AuthService)
        yield
    finally:
        await container.close()


providers: list[Provider] = [
    BaseRequiredInjectionsProvider(),
    DatabaseInjectionsProvider(),
    RabbitInjectionsProvider(),
    AppInjectionsProvider(),
]

if env_config.local_dev:
    providers.append(LocalMockInjectionsProvider())

container = make_async_container(*providers)

app = create_litestar_app(container, lifespan)
