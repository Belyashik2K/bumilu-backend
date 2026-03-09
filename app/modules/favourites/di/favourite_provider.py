from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favourites.application.commands.add import (
    AddToFavouritesCommandHandler,
)
from app.modules.favourites.application.commands.remove import (
    RemoveFromFavouritesCommandHandler,
)
from app.modules.favourites.application.interfaces.entity_resolver import (
    IFavouriteEntityResolver,
)
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.application.queries.get_all_by_user.handler import (
    GetAllFavouritesByUserQueryHandler,
)
from app.modules.favourites.application.queries.readers.favourite import (
    IFavouriteReader,
)
from app.modules.favourites.infrastructure.database.readers.favourite import (
    SQLAlchemyFavouriteReader,
)
from app.modules.favourites.infrastructure.database.repositories.favourite import (
    SQLAlchemyFavouriteRepository,
)
from app.modules.favourites.infrastructure.entity_resolver import (
    FavouriteEntityResolver,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.readers.user import IUserReader


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

    @provide(scope=Scope.REQUEST, provides=IFavouriteReader)
    async def favourite_reader(
        self, session: AsyncSession
    ) -> SQLAlchemyFavouriteReader:
        return SQLAlchemyFavouriteReader(
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    async def get_favourites_by_user_handler(
        self, favourite_reader: IFavouriteReader, user_reader: IUserReader
    ) -> GetAllFavouritesByUserQueryHandler:
        return GetAllFavouritesByUserQueryHandler(
            favourite_reader=favourite_reader,
            user_reader=user_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def add_to_favourites_handler(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
        entity_resolver: IFavouriteEntityResolver,
    ) -> AddToFavouritesCommandHandler:
        return AddToFavouritesCommandHandler(
            favourite_repository=favourite_repository,
            user_repository=user_repository,
            entity_resolver=entity_resolver,
        )

    @provide(scope=Scope.REQUEST)
    async def remove_from_favourites_handler(
        self,
        favourite_repository: IFavouriteRepository,
    ) -> RemoveFromFavouritesCommandHandler:
        return RemoveFromFavouritesCommandHandler(
            favourite_repository=favourite_repository,
        )
