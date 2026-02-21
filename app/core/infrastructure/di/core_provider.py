from dishka import (
    Provider,
    Scope,
    provide,
)

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
