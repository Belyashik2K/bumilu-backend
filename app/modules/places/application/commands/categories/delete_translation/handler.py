from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.application.commands.categories.delete_translation.command import (
    DeletePlaceCategoryTranslationCommand,
)
from app.modules.places.application.exceptions.place_category import (
    PlaceCategoryNotFound,
    PlaceCategoryTranslationNotFound,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)


class DeletePlaceCategoryTranslationCommandHandler(
    ICommandHandler[DeletePlaceCategoryTranslationCommand]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        category_repository: IPlaceCategoryRepository,
        category_translation_repository: IPlaceCategoryTranslationRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_category_repository = category_repository
        self._place_category_translation_repository = category_translation_repository

    async def handle(self, command: DeletePlaceCategoryTranslationCommand) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)
        category = await self._place_category_repository.get_by_id(category_id)
        if category is None:
            raise PlaceCategoryNotFound(category_id=category_id.value)

        category_translation = await self._place_category_translation_repository.get_by_category_id_and_language_code(
            category_id=category_id,
            language_code=command.language_code,
        )
        if category_translation is None:
            raise PlaceCategoryTranslationNotFound(
                category_id=category_id.value,
                language_code=command.language_code,
            )

        category.ensure_translation_can_be_deleted(language_code=command.language_code)
        await self._place_category_translation_repository.delete_by_id(
            category_translation.id
        )
        category.unregister_translation_language(
            language_code=command.language_code
        )  # TODO: think about moving this logic to domain service
        await self._place_category_repository.save(category)
