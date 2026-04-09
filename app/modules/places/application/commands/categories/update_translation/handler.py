from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
)
from app.modules.places.application.commands.categories.update_translation.command import (
    UpdateCategoryTranslationCommand,
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
from app.modules.places.domain.categories.value_objects.name.object import (
    PlaceCategoryNameVO,
)


class UpdateCategoryTranslationCommandHandler(
    ICommandHandler[UpdateCategoryTranslationCommand]
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

    async def handle(self, command: UpdateCategoryTranslationCommand) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)
        category = await self._place_category_repository.get_by_id(category_id)
        if category is None:
            raise PlaceCategoryNotFound(category_id=category_id.value)

        translation = await self._place_category_translation_repository.get_by_category_id_and_language_code(
            category_id, command.language_code
        )
        if translation is None:
            raise PlaceCategoryTranslationNotFound(
                category_id=category_id.value,
                language_code=command.language_code,
            )

        new_name = (
            PlaceCategoryNameVO(command.name) if command.name is not None else None
        )

        translation.update(name=new_name)
        await self._place_category_translation_repository.save(translation)
