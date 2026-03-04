from dishka import Provider, Scope, provide
from fast_depends.msgspec import MsgSpecSerializer
from faststream.rabbit import RabbitBroker

from app.core.config import env_config


class RabbitInjectionsProvider(Provider):
    scope = Scope.APP

    @provide
    def rabbit_broker(self) -> RabbitBroker:
        return RabbitBroker(env_config.rabbit_url, serializer=MsgSpecSerializer())
