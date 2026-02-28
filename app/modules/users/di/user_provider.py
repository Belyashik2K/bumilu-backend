from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.use_cases.get import GetUserUseCase
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

    @provide(scope=Scope.REQUEST)
    async def get_user_uc(
        self,
        user_repository: IUserRepository,
    ) -> GetUserUseCase:
        return GetUserUseCase(
            user_repository=user_repository,
        )
