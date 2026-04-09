from app.core.application.queries import IQueryHandler
from app.modules.places.application.exceptions.place_category import (
    PlaceCategoryNotFound,
)
from app.modules.places.application.queries.categories.admin.get.query import (
    GetAdminPlaceCategoryQuery,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    PlaceCategoryReadModel,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)


class GetAdminPlaceCategoryQueryHandler(
    IQueryHandler[
        GetAdminPlaceCategoryQuery,
        PlaceCategoryReadModel,
    ]
):
    def __init__(
        self,
        place_category_reader: IPlaceCategoryReader,
    ) -> None:
        self._place_category_reader = place_category_reader

    async def handle(self, query: GetAdminPlaceCategoryQuery) -> PlaceCategoryReadModel:
        category = await self._place_category_reader.get_by_id(
            category_id=query.category_id
        )
        if category is None:
            raise PlaceCategoryNotFound(category_id=query.category_id)
        return category
