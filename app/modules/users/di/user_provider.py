from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.get import GetUserQueryHandler
from app.modules.users.application.queries.readers.user import IUserReader
from app.modules.users.infrastructure.database.readers.user import SQLAlchemyUserReader
from app.modules.users.infrastructure.database.repositories.user import (
    SQLAlchemyUserRepository,
)


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IUserRepository)
    async def user_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IUserReader)
    async def user_reader(
        self,
        session: AsyncSession,
    ) -> IUserReader:
        return SQLAlchemyUserReader(
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    async def get_user_handler(
        self,
        user_reader: IUserReader,
    ) -> GetUserQueryHandler:
        return GetUserQueryHandler(
            user_reader=user_reader,
        )
