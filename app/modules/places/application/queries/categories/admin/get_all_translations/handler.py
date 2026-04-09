from app.core.application.queries import IQueryHandler
from app.modules.places.application.queries.categories.admin.get_all_translations.query import (
    GetAdminPlaceCategoryTranslationsListQuery,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    PlaceCategoryTranslationReadModel,
)
from app.modules.places.application.queries.categories.shared.readers.place_category_translation import (
    IPlaceCategoryTranslationReader,
)


class GetAdminPlaceCategoryTranslationsListQueryHandler(
    IQueryHandler[
        GetAdminPlaceCategoryTranslationsListQuery,
        list[PlaceCategoryTranslationReadModel],
    ]
):
    def __init__(
        self, place_category_translation_reader: IPlaceCategoryTranslationReader
    ) -> None:
        self._place_category_translation_reader = place_category_translation_reader

    async def handle(
        self, query: GetAdminPlaceCategoryTranslationsListQuery
    ) -> list[PlaceCategoryTranslationReadModel]:
        translations = (
            await self._place_category_translation_reader.list_by_category_id(
                category_id=query.category_id
            )
        )
        return translations
