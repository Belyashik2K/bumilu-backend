from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.categories.get_all.query import (
    GetAllPlaceCategoriesQuery,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.application.queries.categories.shared.views import (
    PaginatedPlaceCategoriesView,
)


class GetAllPlaceCategoriesQueryHandler(
    IQueryHandler[GetAllPlaceCategoriesQuery, PaginatedPlaceCategoriesView],
):
    def __init__(self, place_category_reader: IPlaceCategoryReader) -> None:
        self._place_category_reader = place_category_reader

    async def handle(
        self, query: GetAllPlaceCategoriesQuery
    ) -> PaginatedPlaceCategoriesView:
        categories = await self._place_category_reader.list(
            limit=query.limit,
            offset=query.offset,
            translation_language=query.language,
        )

        return PaginatedPlaceCategoriesView(
            categories=categories.items,
            pagination=OffsetPagination.create(
                total=categories.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
