from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.application.commands.categories.create_translation.command import (
    CreatePlaceCategoryTranslationCommand,
)
from app.modules.places.application.exceptions.place_category import (
    PlaceCategoryNotFound,
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
        category_repository: IPlaceCategoryRepository,
        category_translation_repository: IPlaceCategoryTranslationRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._category_repository = category_repository
        self._category_translation_repository = category_translation_repository

    async def handle(
        self,
        command: CreatePlaceCategoryTranslationCommand,
    ) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)
        category = await self._category_repository.get_by_id(category_id)
        if category is None:
            raise PlaceCategoryNotFound(category_id=category_id.value)

        new_translation = category.create_translation(
            data=NewPlaceCategoryTranslation(
                language_code=command.language_code,
                name=PlaceCategoryNameVO(command.name),
            )
        )

        await self._category_translation_repository.save(new_translation)
        await self._category_repository.save(category)
