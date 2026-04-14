from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import (
    PaginatedView,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.application.queries.categories.user.get_all.query import (
    GetAllPlaceCategoriesQuery,
)
from app.modules.places.shared.enums.place_category_status import (
    PlaceCategoryStatusEnum,
)


class GetAllPlaceCategoriesQueryHandler(
    IQueryHandler[
        GetAllPlaceCategoriesQuery, PaginatedView[LocalizedPlaceCategoryReadModel]
    ],
):
    def __init__(self, place_category_reader: IPlaceCategoryReader) -> None:
        self._place_category_reader = place_category_reader

    async def handle(
        self, query: GetAllPlaceCategoriesQuery
    ) -> PaginatedView[LocalizedPlaceCategoryReadModel]:
        categories = await self._place_category_reader.list_public_localized(
            limit=query.limit,
            offset=query.offset,
            translation_language=query.language,
            status=PlaceCategoryStatusEnum.PUBLISHED,
        )

        return PaginatedView.create(
            items=categories.items,
            total=categories.total,
            limit=query.limit,
            offset=query.offset,
        )
