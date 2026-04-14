from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.favourites.application.commands.add import (
    AddToFavouritesCommandHandler,
)
from app.modules.favourites.application.commands.remove import (
    RemoveFromFavouritesCommandHandler,
)
from app.modules.favourites.application.interfaces.preview_enricher import (
    IFavouritePreviewEnricher,
)
from app.modules.favourites.application.interfaces.repositories.place_favourite import (
    IPlaceFavouriteRepository,
)
from app.modules.favourites.application.interfaces.target_checker import (
    IFavouriteTargetChecker,
)
from app.modules.favourites.application.interfaces.writers.favourite import (
    IFavouriteWriter,
)
from app.modules.favourites.application.queries.get_all_by_user.handler import (
    GetAllFavouritesByUserQueryHandler,
)
from app.modules.favourites.application.queries.shared.readers import (
    IFavouriteReader,
)
from app.modules.favourites.infrastructure.database.readers.favourite import (
    SQLAlchemyFavouriteReader,
)
from app.modules.favourites.infrastructure.database.repositories.place_favourite import (
    SQLAlchemyPlaceFavouriteRepository,
)
from app.modules.favourites.infrastructure.database.writers.favourite import (
    FavouriteWriter,
)
from app.modules.favourites.infrastructure.preview_enricher import (
    FavouritePreviewEnricher,
)
from app.modules.favourites.infrastructure.preview_providers.place import (
    PlaceFavouritePreviewProvider,
)
from app.modules.favourites.infrastructure.target_checker import (
    FavouriteTargetChecker,
)
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.shared.readers import IUserReader


class FavouriteProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IPlaceFavouriteRepository)
    async def place_favourite_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyPlaceFavouriteRepository:
        return SQLAlchemyPlaceFavouriteRepository(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IFavouriteTargetChecker)
    async def target_checker(
        self,
        place_reader: IPlaceReader,
    ) -> FavouriteTargetChecker:
        return FavouriteTargetChecker(place_reader=place_reader)

    @provide(scope=Scope.REQUEST)
    async def place_preview_provider(
        self,
        place_reader: IPlaceReader,
        storage_url_builder: IFileStorageURLBuilder,
    ) -> PlaceFavouritePreviewProvider:
        return PlaceFavouritePreviewProvider(
            place_reader=place_reader,
            storage_url_builder=storage_url_builder,
        )

    @provide(scope=Scope.REQUEST, provides=IFavouritePreviewEnricher)
    async def favourite_preview_enricher(
        self,
        place_preview_provider: PlaceFavouritePreviewProvider,
    ) -> IFavouritePreviewEnricher:
        return FavouritePreviewEnricher(
            providers=[
                place_preview_provider,
            ]
        )

    @provide(scope=Scope.REQUEST, provides=IFavouriteReader)
    async def favourite_reader(
        self, session: AsyncSession
    ) -> SQLAlchemyFavouriteReader:
        return SQLAlchemyFavouriteReader(
            session=session,
        )

    @provide(scope=Scope.REQUEST, provides=IFavouriteWriter)
    async def favourite_writer(
        self,
        place_favourite_repository: IPlaceFavouriteRepository,
    ) -> FavouriteWriter:
        return FavouriteWriter(place_favourite_repository=place_favourite_repository)

    @provide(scope=Scope.REQUEST)
    async def get_favourites_by_user_handler(
        self,
        favourite_reader: IFavouriteReader,
        user_reader: IUserReader,
        preview_enricher: IFavouritePreviewEnricher,
    ) -> GetAllFavouritesByUserQueryHandler:
        return GetAllFavouritesByUserQueryHandler(
            favourite_reader=favourite_reader,
            user_reader=user_reader,
            preview_enricher=preview_enricher,
        )

    @provide(scope=Scope.REQUEST)
    async def add_to_favourites_handler(
        self,
        favourite_writer: IFavouriteWriter,
        favourite_target_checker: IFavouriteTargetChecker,
        user_repository: IUserRepository,
        transaction_manager: ITransactionManager,
    ) -> AddToFavouritesCommandHandler:
        return AddToFavouritesCommandHandler(
            transaction_manager=transaction_manager,
            favourite_writer=favourite_writer,
            favourite_target_checker=favourite_target_checker,
            user_repository=user_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def remove_from_favourites_handler(
        self,
        favourite_writer: IFavouriteWriter,
        transaction_manager: ITransactionManager,
    ) -> RemoveFromFavouritesCommandHandler:
        return RemoveFromFavouritesCommandHandler(
            transaction_manager=transaction_manager,
            favourite_writer=favourite_writer,
        )
