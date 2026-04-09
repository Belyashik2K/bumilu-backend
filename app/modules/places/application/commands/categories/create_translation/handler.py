from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.application.commands.categories.create_translation.command import (
    CreatePlaceCategoryTranslationCommand,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)
from app.modules.places.domain.categories.models.category_translation.model import (
    NewPlaceCategoryTranslation,
)
from app.modules.places.domain.categories.value_objects.name.object import (
    PlaceCategoryNameVO,
)


class CreatePlaceCategoryTranslationCommandHandler(
    ICommandHandler[CreatePlaceCategoryTranslationCommand]
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

    async def handle(
        self,
        command: CreatePlaceCategoryTranslationCommand,
    ) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)
        category = await self._place_category_repository.get_by_id(category_id)
        if category is None:
            raise ValueError(f"Place category with id {category_id} not found")

        new_translation = category.create_translation(
            data=NewPlaceCategoryTranslation(
                language_code=command.language_code,
                name=PlaceCategoryNameVO(command.name),
            )
        )

        await self._place_category_translation_repository.save(new_translation)
        await self._place_category_repository.save(category)
