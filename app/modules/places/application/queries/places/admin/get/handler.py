from app.core.application.queries import IQueryHandler
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get.query import (
    GetAdminPlaceQuery,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    AdminPlaceDetailsReadModel,
)


class GetAdminPlaceQueryHandler(
    IQueryHandler[GetAdminPlaceQuery, AdminPlaceDetailsReadModel]
):
    def __init__(self, place_reader: IPlaceReader) -> None:
        self._place_reader = place_reader

    async def handle(self, query: GetAdminPlaceQuery) -> AdminPlaceDetailsReadModel:
        place = await self._place_reader.get_admin_details_by_id(
            place_id=query.place_id,
            optional_translation_language=query.language,
        )
        if place is None:
            raise PlaceNotFound(place_id=query.place_id)
        return place
