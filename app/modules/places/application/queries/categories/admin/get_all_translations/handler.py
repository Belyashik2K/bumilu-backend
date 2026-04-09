from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.categories.admin.get_all_translations.query import (
    GetAdminPlaceCategoryTranslationsListQuery,
)
from app.modules.places.application.queries.categories.admin.get_all_translations.view import (
    PaginatedAdminPlaceCategoryTranslationsView,
)
from app.modules.places.application.queries.categories.shared.readers.place_category_translation import (
    IPlaceCategoryTranslationReader,
)


class GetAdminPlaceCategoryTranslationsListQueryHandler(
    IQueryHandler[
        GetAdminPlaceCategoryTranslationsListQuery,
        PaginatedAdminPlaceCategoryTranslationsView,
    ]
):
    def __init__(
        self, place_category_translation_reader: IPlaceCategoryTranslationReader
    ) -> None:
        self._place_category_translation_reader = place_category_translation_reader

    async def handle(
        self, query: GetAdminPlaceCategoryTranslationsListQuery
    ) -> PaginatedAdminPlaceCategoryTranslationsView:
        translations = (
            await self._place_category_translation_reader.list_by_category_id(
                category_id=query.category_id,
                limit=query.limit,
                offset=query.offset,
            )
        )
        return PaginatedAdminPlaceCategoryTranslationsView(
            translations=translations.items,
            pagination=OffsetPagination.create(
                total=translations.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
