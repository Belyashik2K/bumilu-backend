from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favourites.application.interfaces.entity_resolver import (
    IFavouriteEntityResolver,
)
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.application.use_cases.add import AddToFavouritesUseCase
from app.modules.favourites.application.use_cases.get_all_by_user import (
    GetAllFavouritesByUserUseCase,
)
from app.modules.favourites.infrastructure.database.repositories.favourite import (
    SQLAlchemyFavouriteRepository,
)
from app.modules.favourites.infrastructure.entity_resolver import (
    FavouriteEntityResolver,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository


class FavouriteProvider(Provider):
    @provide(scope=Scope.APP, provides=IFavouriteEntityResolver)
    async def entity_resolver(
        self,
    ) -> FavouriteEntityResolver:
        return FavouriteEntityResolver()

    @provide(scope=Scope.REQUEST, provides=IFavouriteRepository)
    async def favourite_repository(
        self, session: AsyncSession
    ) -> SQLAlchemyFavouriteRepository:
        return SQLAlchemyFavouriteRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    async def get_favourites_by_user_uc(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
    ) -> GetAllFavouritesByUserUseCase:
        return GetAllFavouritesByUserUseCase(
            favourite_repository=favourite_repository,
            user_repository=user_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def add_to_favourites_uc(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
        entity_resolver: IFavouriteEntityResolver,
    ) -> AddToFavouritesUseCase:
        return AddToFavouritesUseCase(
            favourite_repository=favourite_repository,
            user_repository=user_repository,
            entity_resolver=entity_resolver,
        )

    @provide(scope=Scope.REQUEST)
    async def remove_from_favourites_uc(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
        entity_resolver: IFavouriteEntityResolver,
    ) -> AddToFavouritesUseCase:
        return AddToFavouritesUseCase(
            favourite_repository=favourite_repository,
            user_repository=user_repository,
            entity_resolver=entity_resolver,
        )
