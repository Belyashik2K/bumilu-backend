from app.core.application.queries import IQueryHandler
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get_photos.query import (
    GetAdminPlacePhotosQuery,
)
from app.modules.places.application.queries.places.admin.get_photos.view import (
    AdminPlacePhotoView,
)
from app.modules.places.application.queries.places.shared.views import PlacePhotoView


class GetAdminPlacePhotosQueryHandler(
    IQueryHandler[GetAdminPlacePhotosQuery, list[PlacePhotoView]]
):
    def __init__(
        self, place_reader: IPlaceReader, storage_url_builder: IFileStorageURLBuilder
    ) -> None:
        self._place_reader = place_reader
        self._storage_url_builder = storage_url_builder

    async def handle(
        self, query: GetAdminPlacePhotosQuery
    ) -> list[AdminPlacePhotoView]:
        photos = await self._place_reader.get_admin_photos_by_id(
            place_id=query.place_id
        )

        # TODO: add more metadata to photos (e.g. is_main, order, etc.)
        # TODO: think about photos in statuses like "hidden", "deleted", etc.

        return [
            AdminPlacePhotoView.from_read_model(
                photo, storage_url_builder=self._storage_url_builder
            )
            for photo in photos
        ]
