from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.application.interfaces.transaction_manager import ITransactionManager
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
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)


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
