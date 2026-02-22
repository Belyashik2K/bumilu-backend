from collections.abc import AsyncIterator

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.config import AppConfig
from app.core.infrastructure.database.helper import SQLAlchemyDatabaseHelper


class CoreProvider(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> AppConfig:
        return AppConfig()  # type: ignore[call-arg]

    @provide(scope=Scope.APP)
    def database_helper(
        self,
        config: AppConfig,
    ) -> SQLAlchemyDatabaseHelper:
        return SQLAlchemyDatabaseHelper(
            dsn=config.database.dsn,
            echo=config.database.echo,
            echo_pool=config.database.echo_pool,
            pool_size=config.database.pool_size,
            max_overflow=config.database.max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    async def database_session(
        self,
        database_helper: SQLAlchemyDatabaseHelper,
    ) -> AsyncIterator[AsyncSession]:
        async with (
            database_helper.session_factory() as session,
            session.begin(),
        ):
            yield session
