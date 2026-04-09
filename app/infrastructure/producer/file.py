import uuid
from dataclasses import dataclass

from faststream.rabbit import RabbitBroker

from app.core.application.dto.file import FileIdMessage
from app.core.application.interfaces.producer.file import IImageOptimizeProducer


@dataclass
class ImageOptimizeRabbitProducer(IImageOptimizeProducer):
    _rabbit_broker: RabbitBroker

    async def send(self, file_id: uuid.UUID) -> None:
        await self._rabbit_broker.publish(FileIdMessage(file_id=file_id), queue="image-optimize")
