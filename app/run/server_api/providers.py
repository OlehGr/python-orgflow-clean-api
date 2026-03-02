from dishka import Provider, Scope, provide

from app.core.application.interfaces.common.background import IBackgroundExecutor
from app.core.application.interfaces.common.events import IEntityEventBus
from app.core.application.interfaces.projection.user import IUserProjection
from app.core.application.interfaces.repository.entity_event import IEntityEventRepository
from app.core.application.interfaces.repository.user import IUserRepository
from app.core.application.interfaces.services.email import IEmailService
from app.core.application.interfaces.services.tokens import ITokensService
from app.core.application.services.auth import AuthService
from app.core.application.services.entity_event import EntityEventService
from app.core.application.services.user import UserService
from app.infrastructure.common.background import BackgroundExecutor
from app.infrastructure.common.event_bus import InMemoryEntityEventBus
from app.infrastructure.database.projection.user import UserProjection
from app.infrastructure.database.repository.entity_event import EntityEventRepository
from app.infrastructure.database.repository.user import UserRepository
from app.infrastructure.services.email.local import LoggerEmailService
from app.infrastructure.services.tokens.jwt import JwtService


class AppInjectionsProvider(Provider):
    scope = Scope.APP

    background_executor = provide(BackgroundExecutor, provides=IBackgroundExecutor)

    tokens_service = provide(JwtService, provides=ITokensService)
    email_service = provide(LoggerEmailService, provides=IEmailService)

    user_repository = provide(UserRepository, provides=IUserRepository)
    user_projection = provide(UserProjection, provides=IUserProjection)
    user_service = provide(UserService)

    auth_service = provide(AuthService)

    entity_event_repository = provide(EntityEventRepository, provides=IEntityEventRepository)
    entity_event_service = provide(EntityEventService)
    entity_event_bus = provide(InMemoryEntityEventBus, provides=IEntityEventBus)
