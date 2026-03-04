from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import make_container
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.core.application.services.entity_event import EntityEventService
from app.core.application.services.file import FileOptimizeService
from app.infrastructure.database.providers import DatabaseInjectionsProvider
from app.infrastructure.producer.file import FileCompressMessage
from app.infrastructure.rabbit.broker import RabbitInjectionsProvider
from app.run.shared.providers import BaseRequiredInjectionsProvider
from .providers import AppInjectionsProvider


container = make_container(
    BaseRequiredInjectionsProvider(), DatabaseInjectionsProvider(), RabbitInjectionsProvider(), AppInjectionsProvider()
)


broker = container.get(RabbitBroker)


@broker.subscriber("file-compress")
async def compress_file(data: FileCompressMessage) -> None:
    file_optimize_service = container.get(FileOptimizeService)
    await file_optimize_service.compress_file(data.file_id)


@asynccontextmanager
async def lifespan() -> AsyncIterator:
    container.get(EntityEventService)
    yield
    container.close()


app = FastStream(broker, lifespan=lifespan)
