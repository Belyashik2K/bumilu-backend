from app.core.application.queries import IQueryHandler
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get_map_poi.query import (
    GetAdminPlacesMapPOIQuery,
)
from app.modules.places.application.queries.places.shared.models.place_map_poi import (
    AdminPlaceMapPOIReadModel,
)


class GetAdminPlacesMapPOIQueryHandler(
    IQueryHandler[
        GetAdminPlacesMapPOIQuery,
        list[AdminPlaceMapPOIReadModel],
    ]
):
    def __init__(self, place_reader: IPlaceReader) -> None:
        self._place_reader = place_reader

    async def handle(
        self, query: GetAdminPlacesMapPOIQuery
    ) -> list[AdminPlaceMapPOIReadModel]:
        return await self._place_reader.list_admin_poi_in_bounds(
            bounds=query.bounds,
            translation_language=query.language,
            limit=query.limit,
        )
