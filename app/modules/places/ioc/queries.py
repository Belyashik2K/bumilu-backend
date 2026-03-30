from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.places.application.queries.categories.get_all.handler import (
    GetAllPlaceCategoriesQueryHandler,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)


class PlacesQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_all_place_categories_handler(
        self, place_category_reader: IPlaceCategoryReader
    ) -> "GetAllPlaceCategoriesQueryHandler":
        return GetAllPlaceCategoriesQueryHandler(
            place_category_reader=place_category_reader,
        )
