from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import (
    PaginatedView,
)
from app.modules.places.application.exceptions.place_category import (
    PlaceCategoryNotFound,
)
from app.modules.places.application.queries.categories.admin.get_all_translations.query import (
    GetAdminPlaceCategoryTranslationsListQuery,
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


class GetAdminPlaceCategoryTranslationsListQueryHandler(
    IQueryHandler[
        GetAdminPlaceCategoryTranslationsListQuery,
        PaginatedView[PlaceCategoryTranslationReadModel],
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
        self, query: GetAdminPlaceCategoryTranslationsListQuery
    ) -> PaginatedView[PlaceCategoryTranslationReadModel]:
        exists = await self._place_category_reader.exists_by_id(
            category_id=query.category_id
        )
        if not exists:
            raise PlaceCategoryNotFound(category_id=query.category_id)

        translations = (
            await self._place_category_translation_reader.list_by_category_id(
                category_id=query.category_id,
                limit=query.limit,
                offset=query.offset,
            )
        )
        return PaginatedView.create(
            items=translations.items,
            total=translations.total,
            limit=query.limit,
            offset=query.offset,
        )
