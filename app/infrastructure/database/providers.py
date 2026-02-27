from collections.abc import Iterator

from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.core.application.interfaces.managers.transaction import ITransactionManager
from app.core.config import env_config
from app.infrastructure.database.internal.transaction import (
    TransactionalSession,
    TransactionalSessionFactory,
    TransactionManager,
)


class DatabaseInjectionsProvider(Provider):
    scope = Scope.APP

    @provide
    def engine(self) -> Iterator[AsyncEngine]:
        engine = create_async_engine(
            env_config.database_url,
            pool_size=env_config.db_pool_size,
            max_overflow=env_config.db_max_overflow,
            pool_timeout=60,
            pool_pre_ping=True,
        )
        yield engine

    @provide
    def session_factory(self, engine: AsyncEngine) -> TransactionalSessionFactory:
        return async_sessionmaker(
            bind=engine,
            class_=TransactionalSession,
            expire_on_commit=True,
            autoflush=False,
        )

    transaction_manager_impl = provide(TransactionManager)
    transaction_manager = alias(source=TransactionManager, provides=ITransactionManager)
