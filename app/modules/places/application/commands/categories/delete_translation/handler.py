from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.application.commands.categories.delete_translation.command import (
    DeleteCategoryTranslationCommand,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)


class DeleteCategoryTranslationCommandHandler(
    ICommandHandler[DeleteCategoryTranslationCommand]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_category_repository: IPlaceCategoryRepository,
        place_category_translation_repository: IPlaceCategoryTranslationRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_category_repository = place_category_repository
        self._place_category_translation_repository = (
            place_category_translation_repository
        )

    async def handle(self, command: DeleteCategoryTranslationCommand) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)
        category = await self._place_category_repository.get_by_id(category_id)
        if category is None:
            raise ValueError(f"Place category with id {category_id} not found")

        category_translation = await self._place_category_translation_repository.get_by_category_id_and_language_code(
            category_id=category_id,
            language_code=command.language_code,
        )
        if category_translation is None:
            raise ValueError(
                f"Translation for place category with id {category_id} and language code {command.language_code} not found"
            )

        category.ensure_translation_can_be_deleted(language_code=command.language_code)
        await self._place_category_translation_repository.delete_by_id(
            category_translation.id
        )
        category.unregister_translation_language(
            language_code=command.language_code
        )  # TODO: think about moving this logic to domain service
        await self._place_category_repository.save(category)
