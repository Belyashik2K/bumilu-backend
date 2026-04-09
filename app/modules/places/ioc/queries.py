from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.application.queries.categories.user.get_all import (
    GetAllPlaceCategoriesQueryHandler,
)
from app.modules.places.application.queries.places.get.handler import (
    GetPlaceQueryHandler,
)
from app.modules.places.application.queries.places.get_all.handler import (
    GetAllPlacesQueryHandler,
)
from app.modules.places.application.queries.places.get_map_poi.handler import (
    GetPlacesMapPOIQueryHandler,
)


class PlacesQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_all_place_categories_handler(
        self, place_category_reader: IPlaceCategoryReader
    ) -> GetAllPlaceCategoriesQueryHandler:
        return GetAllPlaceCategoriesQueryHandler(
            place_category_reader=place_category_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_place_handler(
        self, place_reader: IPlaceReader
    ) -> GetPlaceQueryHandler:
        return GetPlaceQueryHandler(
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_all_places_handler(
        self, place_reader: IPlaceReader
    ) -> GetAllPlacesQueryHandler:
        return GetAllPlacesQueryHandler(
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_places_map_poi_handler(
        self, place_reader: IPlaceReader
    ) -> GetPlacesMapPOIQueryHandler:
        return GetPlacesMapPOIQueryHandler(
            place_reader=place_reader,
        )
