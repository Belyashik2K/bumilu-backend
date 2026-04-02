from app.core.application.queries import IQueryHandler
from app.modules.places.application.queries.places.get.query import GetPlaceQuery
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import PlaceView


class GetPlaceQueryHandler(
    IQueryHandler[
        GetPlaceQuery,
        PlaceView,
    ]
):
    def __init__(self, place_reader: IPlaceReader) -> None:
        self._place_reader = place_reader

    async def handle(self, query: GetPlaceQuery) -> PlaceView:
        place = await self._place_reader.get_by_id(
            place_id=query.place_id, translation_language=query.language
        )
        if place is None:
            raise ValueError("Place not found")  # TODO: custom exception
        return place
