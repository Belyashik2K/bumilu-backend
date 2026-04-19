from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import DataListView
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import (
    PlaceMapPOICategoryView,
    PlaceMapPOIView,
)
from app.modules.places.application.queries.places.user.get_map_poi.query import (
    GetPlacesMapPOIQuery,
)


class GetPlacesMapPOIQueryHandler(
    IQueryHandler[
        GetPlacesMapPOIQuery,
        DataListView[PlaceMapPOIView],
    ]
):
    def __init__(
        self,
        place_reader: IPlaceReader,
    ) -> None:
        self._place_reader = place_reader

    async def handle(
        self, query: GetPlacesMapPOIQuery
    ) -> DataListView[PlaceMapPOIView]:
        query.bounds.validate()

        pois = await self._place_reader.list_poi_in_bounds(
            bounds=query.bounds,
            translation_language=query.language,
            limit=query.limit,
        )

        return DataListView.create(
            [
                PlaceMapPOIView(
                    id=poi.id,
                    category=PlaceMapPOICategoryView(
                        id=poi.category.id,
                        name=poi.category.name,
                        marker_color=poi.category.marker_color,
                        icon_key=poi.category.icon_key,
                    ),
                    title=poi.title,
                    location=poi.location,
                )
                for poi in pois
            ]
        )
