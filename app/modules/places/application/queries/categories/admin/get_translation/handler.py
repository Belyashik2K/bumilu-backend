from app.core.application.queries import IQueryHandler
from app.modules.places.application.exceptions.place_category import (
    PlaceCategoryNotFound,
    PlaceCategoryTranslationNotFound,
)
from app.modules.places.application.queries.categories.admin.get_translation.query import (
    GetAdminPlaceCategoryTranslationQuery,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    PlaceCategoryTranslationReadModel,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.application.queries.categories.shared.readers.place_category_translation import (
    IPlaceCategoryTranslationReader,
)


class GetAdminPlaceCategoryTranslationQueryHandler(
    IQueryHandler[
        GetAdminPlaceCategoryTranslationQuery, PlaceCategoryTranslationReadModel
    ]
):
    def __init__(
        self,
        place_category_reader: IPlaceCategoryReader,
        place_category_translation_reader: IPlaceCategoryTranslationReader,
    ) -> None:
        self._place_category_reader = place_category_reader
        self._place_category_translation_reader = place_category_translation_reader

    async def handle(
        self, query: GetAdminPlaceCategoryTranslationQuery
    ) -> PlaceCategoryTranslationReadModel:
        exists = await self._place_category_reader.exists_by_id(
            category_id=query.category_id
        )
        if not exists:
            raise PlaceCategoryNotFound(category_id=query.category_id)

        translation = await self._place_category_translation_reader.get_by_category_id_and_language_code(
            category_id=query.category_id, language_code=query.language_code
        )
        if translation is None:
            raise PlaceCategoryTranslationNotFound(
                category_id=query.category_id, language_code=query.language_code
            )
        return translation
