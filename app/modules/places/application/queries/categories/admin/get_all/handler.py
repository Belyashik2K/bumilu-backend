from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import (
    PaginatedView,
)
from app.modules.places.application.queries.categories.admin.get_all.query import (
    GetAdminPlaceCategoriesListQuery,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    AdminPlaceCategoryReadModel,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)


class GetAdminPlaceCategoriesListQueryHandler(
    IQueryHandler[
        GetAdminPlaceCategoriesListQuery, PaginatedView[AdminPlaceCategoryReadModel]
    ]
):
    def __init__(self, place_category_reader: IPlaceCategoryReader) -> None:
        self._place_category_reader = place_category_reader

    async def handle(
        self, query: GetAdminPlaceCategoriesListQuery
    ) -> PaginatedView[AdminPlaceCategoryReadModel]:
        categories = await self._place_category_reader.list_admin(
            limit=query.limit,
            offset=query.offset,
            optional_translation_language=query.language,
            status=None,  # TODO: add filtering by status (e.g. only published categories)
        )

        return PaginatedView.create(
            items=categories.items,
            total=categories.total,
            limit=query.limit,
            offset=query.offset,
        )
