from dishka import Provider, Scope, provide

from app.core.application.interfaces.common.background import IBackgroundExecutor
from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.repository.entity_event import IEntityEventRepository
from app.core.application.listeners.entity_event_save import EntityEventSaveListener
from app.infrastructure.common.background import BackgroundExecutor
from app.infrastructure.common.event_bus import InMemoryEntityEventBus
from app.infrastructure.database.repository.entity_event import EntityEventRepository


class BaseRequiredInjectionsProvider(Provider):
    scope = Scope.APP

    background_executor = provide(BackgroundExecutor, provides=IBackgroundExecutor)

    entity_event_repository = provide(EntityEventRepository, provides=IEntityEventRepository)
    entity_event_save_listener = provide(EntityEventSaveListener)
    entity_event_bus = provide(InMemoryEntityEventBus, provides=IEntityEventBus)
