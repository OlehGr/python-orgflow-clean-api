from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import make_container
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.core.application.listeners.entity_event_save import EntityEventSaveListener
from app.core.application.services.file import ImageOptimizeService
from app.infrastructure.database.providers import DatabaseInjectionsProvider
from app.infrastructure.producer.file import FileIdMessage
from app.infrastructure.rabbit.broker import RabbitInjectionsProvider
from app.run.shared.providers import BaseRequiredInjectionsProvider
from .providers import AppInjectionsProvider


container = make_container(
    BaseRequiredInjectionsProvider(), DatabaseInjectionsProvider(), RabbitInjectionsProvider(), AppInjectionsProvider()
)


broker = container.get(RabbitBroker)


@broker.subscriber("image-optimize")
async def compress_file(data: FileIdMessage) -> None:
    image_optimize_service = container.get(ImageOptimizeService)
    await image_optimize_service.compress_file(data.file_id)


@asynccontextmanager
async def lifespan() -> AsyncIterator:
    container.get(EntityEventSaveListener)
    yield
    container.close()


app = FastStream(broker, lifespan=lifespan)
