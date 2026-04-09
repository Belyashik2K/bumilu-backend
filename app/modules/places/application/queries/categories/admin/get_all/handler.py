from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.admin.get_all.query import (
    GetAdminCategoriesListQuery,
)
from app.modules.places.application.queries.categories.admin.get_all.view import (
    PaginatedAdminPlaceCategoriesView,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)


class GetAdminCategoriesListQueryHandler(
    IQueryHandler[GetAdminCategoriesListQuery, PaginatedAdminPlaceCategoriesView]
):
    def __init__(self, place_category_reader: IPlaceCategoryReader) -> None:
        self._place_category_reader = place_category_reader

    async def handle(
        self, query: GetAdminCategoriesListQuery
    ) -> PaginatedAdminPlaceCategoriesView:
        # TODO: add more information to the view, e.g. number of places in each category
        categories = await self._place_category_reader.list(
            limit=query.limit,
            offset=query.offset,
            translation_language=LanguageEnum.RU,
            # TODO: mock language for now, need to add support of multiple languages in admin panel
        )

        return PaginatedAdminPlaceCategoriesView(
            categories=categories.items,
            pagination=OffsetPagination.create(
                total=categories.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
