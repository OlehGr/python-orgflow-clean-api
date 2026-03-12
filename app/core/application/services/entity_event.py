from dataclasses import dataclass

import msgspec

from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.repository.entity_event import IEntityEventRepository
from app.core.models import EntityEventModel
from app.core.models.entity_event import EntityEvent


@dataclass
class EntityEventService:
    _entity_event_bus: IEntityEventBus
    _entity_event_repository: IEntityEventRepository

    def __post_init__(self) -> None:
        self._entity_event_bus.subscribe("*", self.save_entity_event)

    async def save_entity_event(self, entity_event: EntityEvent) -> None:
        event = EntityEventModel.create(
            event_id=entity_event.id,
            entity=entity_event.entity,
            entity_id=entity_event.entity_id,
            subject=entity_event.subject,
            producer_id=entity_event.producer_id,
            data=msgspec.to_builtins(entity_event.data),
        )
        await self._entity_event_repository.save(event)
