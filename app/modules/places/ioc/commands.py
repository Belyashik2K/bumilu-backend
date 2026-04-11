from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.places.application.commands.categories.change_status.handler import (
    ChangePlaceCategoryStatusCommandHandler,
)
from app.modules.places.application.commands.categories.create.handler import (
    CreatePlaceCategoryCommandHandler,
)
from app.modules.places.application.commands.categories.create_translation.handler import (
    CreatePlaceCategoryTranslationCommandHandler,
)
from app.modules.places.application.commands.categories.delete.handler import (
    DeletePlaceCategoryCommandHandler,
)
from app.modules.places.application.commands.categories.delete_translation.handler import (
    DeletePlaceCategoryTranslationCommandHandler,
)
from app.modules.places.application.commands.categories.update.handler import (
    UpdatePlaceCategoryCommandHandler,
)
from app.modules.places.application.commands.categories.update_translation.handler import (
    UpdatePlaceCategoryTranslationCommandHandler,
)
from app.modules.places.application.commands.places.add_phone.handler import (
    AddPlacePhoneCommandHandler,
)
from app.modules.places.application.commands.places.create.handler import (
    CreatePlaceCommandHandler,
)
from app.modules.places.application.commands.places.create_translation.handler import (
    CreatePlaceTranslationCommandHandler,
)
from app.modules.places.application.commands.places.delete.handler import (
    DeletePlaceCommandHandler,
)
from app.modules.places.application.commands.places.delete_phone.handler import (
    DeletePlacePhoneCommandHandler,
)
from app.modules.places.application.commands.places.delete_translation.command import (
    DeletePlaceTranslationCommandHandler,
)
from app.modules.places.application.commands.places.make_phone_primary.handler import (
    MakePlacePhonePrimaryCommandHandler,
)
from app.modules.places.application.commands.places.update.handler import (
    UpdatePlaceCommandHandler,
)
from app.modules.places.application.commands.places.update_phone.handler import (
    UpdatePlacePhoneCommandHandler,
)
from app.modules.places.application.commands.places.update_translation.handler import (
    UpdatePlaceTranslationCommandHandler,
)
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)
from app.modules.places.application.interfaces.repositories.place_translation import (
    IPlaceTranslationRepository,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.routes.application.interfaces.readers.route import IRouteReader


class PlacesCommandHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def create_category_handler(
        self,
        category_repository: IPlaceCategoryRepository,
        category_reader: IPlaceCategoryReader,
        category_translation_repository: IPlaceCategoryTranslationRepository,
        transaction_manager: ITransactionManager,
    ) -> CreatePlaceCategoryCommandHandler:
        return CreatePlaceCategoryCommandHandler(
            category_repository=category_repository,
            category_reader=category_reader,
            category_translation_repository=category_translation_repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def create_category_translation_handler(
        self,
        category_repository: IPlaceCategoryRepository,
        category_translation_repository: IPlaceCategoryTranslationRepository,
        transaction_manager: ITransactionManager,
    ) -> CreatePlaceCategoryTranslationCommandHandler:
        return CreatePlaceCategoryTranslationCommandHandler(
            category_repository=category_repository,
            category_translation_repository=category_translation_repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_category_handler(
        self,
        place_reader: IPlaceReader,
        category_repository: IPlaceCategoryRepository,
        transaction_manager: ITransactionManager,
    ) -> DeletePlaceCategoryCommandHandler:
        return DeletePlaceCategoryCommandHandler(
            place_reader=place_reader,
            category_repository=category_repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_category_translation_handler(
        self,
        category_repository: IPlaceCategoryRepository,
        category_translation_repository: IPlaceCategoryTranslationRepository,
        transaction_manager: ITransactionManager,
    ) -> DeletePlaceCategoryTranslationCommandHandler:
        return DeletePlaceCategoryTranslationCommandHandler(
            category_repository=category_repository,
            category_translation_repository=category_translation_repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def update_category_handler(
        self,
        category_repository: IPlaceCategoryRepository,
        category_reader: IPlaceCategoryReader,
        transaction_manager: ITransactionManager,
    ) -> UpdatePlaceCategoryCommandHandler:
        return UpdatePlaceCategoryCommandHandler(
            place_category_repository=category_repository,
            place_category_reader=category_reader,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def update_category_translation_handler(
        self,
        category_repository: IPlaceCategoryRepository,
        category_translation_repository: IPlaceCategoryTranslationRepository,
        transaction_manager: ITransactionManager,
    ) -> UpdatePlaceCategoryTranslationCommandHandler:
        return UpdatePlaceCategoryTranslationCommandHandler(
            place_category_repository=category_repository,
            place_category_translation_repository=category_translation_repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def change_place_category_status_handler(
        self,
        category_repository: IPlaceCategoryRepository,
        transaction_manager: ITransactionManager,
    ) -> ChangePlaceCategoryStatusCommandHandler:
        return ChangePlaceCategoryStatusCommandHandler(
            place_category_repository=category_repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def create_place_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_category_repository: IPlaceCategoryRepository,
    ) -> CreatePlaceCommandHandler:
        return CreatePlaceCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
            place_category_repository=place_category_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def update_place_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_category_repository: IPlaceCategoryRepository,
    ) -> UpdatePlaceCommandHandler:
        return UpdatePlaceCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
            place_category_repository=place_category_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_place_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        route_reader: IRouteReader,
    ) -> DeletePlaceCommandHandler:
        return DeletePlaceCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
            route_reader=route_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def create_place_translation_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_translation_repository: IPlaceTranslationRepository,
    ) -> CreatePlaceTranslationCommandHandler:
        return CreatePlaceTranslationCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
            place_translation_repository=place_translation_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def update_place_translation_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_translation_repository: IPlaceTranslationRepository,
    ) -> UpdatePlaceTranslationCommandHandler:
        return UpdatePlaceTranslationCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
            place_translation_repository=place_translation_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_place_translation_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_translation_repository: IPlaceTranslationRepository,
    ) -> DeletePlaceTranslationCommandHandler:
        return DeletePlaceTranslationCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
            place_translation_repository=place_translation_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def add_place_phone_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
    ) -> AddPlacePhoneCommandHandler:
        return AddPlacePhoneCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_place_phone_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
    ) -> DeletePlacePhoneCommandHandler:
        return DeletePlacePhoneCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def update_place_phone_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
    ) -> UpdatePlacePhoneCommandHandler:
        return UpdatePlacePhoneCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def make_phone_primary_handler(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
    ) -> MakePlacePhonePrimaryCommandHandler:
        return MakePlacePhonePrimaryCommandHandler(
            transaction_manager=transaction_manager,
            place_repository=place_repository,
        )
