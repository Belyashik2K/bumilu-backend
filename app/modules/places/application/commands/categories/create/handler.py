from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.places.application.commands.categories.create.command import (
    CreatePlaceCategoryCommand,
    CreatePlaceCategoryCommandResult,
)
from app.modules.places.application.exceptions.place_category import (
    PlaceCategoryAlreadyExists,
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
from app.modules.places.domain.categories.models.category.model import PlaceCategory
from app.modules.places.domain.categories.models.category_translation.model import (
    NewPlaceCategoryTranslation,
)
from app.modules.places.domain.categories.value_objects.icon_key import (
    PlaceCategoryIconKeyVO,
)
from app.modules.places.domain.categories.value_objects.marker_color.object import (
    PlaceCategoryMarkerColorVO,
)
from app.modules.places.domain.categories.value_objects.name.object import (
    PlaceCategoryNameVO,
)
from app.modules.places.domain.categories.value_objects.slug import PlaceCategorySlugVO


class CreatePlaceCategoryCommandHandler(
    ICommandHandlerWithResult[
        CreatePlaceCategoryCommand,
        CreatePlaceCategoryCommandResult,
    ]
):
    def __init__(
        self,
        category_repository: IPlaceCategoryRepository,
        category_reader: IPlaceCategoryReader,
        category_translation_repository: IPlaceCategoryTranslationRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._category_repository = category_repository
        self._category_reader = category_reader
        self._category_translation_repository = category_translation_repository

    async def handle(
        self,
        command: CreatePlaceCategoryCommand,
    ) -> CreatePlaceCategoryCommandResult:
        if await self._category_reader.exists(slug=command.slug):
            raise PlaceCategoryAlreadyExists(slug=command.slug)

        slug = PlaceCategorySlugVO(command.slug)
        icon_key = PlaceCategoryIconKeyVO(command.icon_key)
        marker_color = PlaceCategoryMarkerColorVO(command.marker_color)

        translations = [
            NewPlaceCategoryTranslation(
                language_code=translation.language_code,
                name=PlaceCategoryNameVO(translation.name),
            )
            for translation in command.translations
        ]

        category, created_translations = PlaceCategory.create(
            slug=slug,
            icon_key=icon_key,
            marker_color=marker_color,
            translations=translations,
        )

        await self._category_repository.save(category)
        await self._category_translation_repository.save_many(created_translations)

        return CreatePlaceCategoryCommandResult(id=category.id.value)
