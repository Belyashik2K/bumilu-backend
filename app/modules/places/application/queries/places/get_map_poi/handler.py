from app.core.application.queries import IQueryHandler
from app.modules.places.application.queries.places.get_map_poi.query import (
    GetPlacesMapPOIQuery,
)
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import PlaceMapPOIView


class GetPlacesMapPOIQueryHandler(
    IQueryHandler[
        GetPlacesMapPOIQuery,
        list[PlaceMapPOIView],
    ]
):
    def __init__(
        self,
        place_reader: IPlaceReader,
    ) -> None:
        self._place_reader = place_reader

    async def handle(self, query: GetPlacesMapPOIQuery) -> list[PlaceMapPOIView]:
        query.bounds.validate()
        return await self._place_reader.list_poi_in_bounds(
            bounds=query.bounds,
            translation_language=query.language,
            limit=query.limit,
        )
