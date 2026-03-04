from collections.abc import AsyncIterator

from dishka import (
    Provider,
    Scope,
    provide,
)
from redis.asyncio import Redis
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
            echo_pool=config.database.pool.echo,
            pool_size=config.database.pool.size,
            max_overflow=config.database.pool.max_overflow,
        )

    @provide(scope=Scope.APP)
    async def redis_client(
        self,
        config: AppConfig,
    ) -> Redis:
        return Redis(
            username=config.redis.username,
            password=config.redis.password,
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
        )

    @provide(scope=Scope.REQUEST)
    async def database_session(
        self,
        database_helper: SQLAlchemyDatabaseHelper,
    ) -> AsyncIterator[AsyncSession]:
        session = database_helper.session_factory()
        try:
            yield session
        finally:
            await session.close()
