from app.core.application.queries import IQueryHandler
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import (
    PlacePhotoView,
    PlaceView,
)
from app.modules.places.application.queries.places.user.get.query import GetPlaceQuery


class GetPlaceQueryHandler(
    IQueryHandler[
        GetPlaceQuery,
        PlaceView,
    ]
):
    def __init__(
        self,
        place_reader: IPlaceReader,
        storage_url_builder: IFileStorageURLBuilder,
    ) -> None:
        self._place_reader = place_reader
        self._storage_url_builder = storage_url_builder

    async def handle(self, query: GetPlaceQuery) -> PlaceView:
        place = await self._place_reader.get_by_id(
            actor_id=query.actor_id,
            place_id=query.place_id,
            translation_language=query.language,
        )
        if place is None:
            raise PlaceNotFound(place_id=query.place_id)

        return PlaceView(
            id=place.id,
            title=place.title,
            description=place.description,
            short_description=place.short_description,
            timezone=place.timezone,
            category=place.category,
            photos=[
                PlacePhotoView.from_read_model(
                    read_model=photo,
                    storage_url_builder=self._storage_url_builder,
                )
                for photo in place.photos
            ],
            address=place.address,
            location=place.location,
            rating=place.rating,
            phones=place.phones,
            working_days=place.working_days,
            user_context=place.user_context,
        )
