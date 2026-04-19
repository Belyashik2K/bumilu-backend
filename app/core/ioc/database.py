from collections.abc import AsyncIterator

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.infrastructure.config import AppConfig
from app.core.infrastructure.database.helper import SQLAlchemyDatabaseHelper
from app.core.infrastructure.database.transaction_manager import (
    SQLAlchemyTransactionManager,
)


class DatabaseProvider(Provider):
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

    @provide(scope=Scope.REQUEST)
    async def database_session(
        self,
        database_helper: SQLAlchemyDatabaseHelper,
    ) -> AsyncIterator[AsyncSession]:
        async with database_helper.session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST, provides=ITransactionManager)
    async def transaction_manager(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyTransactionManager:
        return SQLAlchemyTransactionManager(session=session)
