import uuid
from dataclasses import dataclass

import msgspec
from faststream.rabbit import RabbitBroker

from app.core.application.interfaces.producer.file import IFileCompressProducer


class FileCompressMessage(msgspec.Struct, frozen=True):
    file_id: uuid.UUID


@dataclass
class RabbitFileCompressProducer(IFileCompressProducer):
    _rabbit_broker: RabbitBroker

    async def send(self, file_id: uuid.UUID) -> None:
        await self._rabbit_broker.publish(FileCompressMessage(file_id=file_id), queue="file-compress")
