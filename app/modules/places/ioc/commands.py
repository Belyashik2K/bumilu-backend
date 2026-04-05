from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.places.application.commands.categories.create.handler import (
    CreatePlaceCategoryCommandHandler,
)
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
