from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import DataListView
from app.modules.places.application.exceptions.place import PlaceNotFound
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


class GetAdminPlacePhotosQueryHandler(
    IQueryHandler[GetAdminPlacePhotosQuery, DataListView[AdminPlacePhotoView]]
):
    def __init__(
        self, place_reader: IPlaceReader, storage_url_builder: IFileStorageURLBuilder
    ) -> None:
        self._place_reader = place_reader
        self._storage_url_builder = storage_url_builder

    async def handle(
        self, query: GetAdminPlacePhotosQuery
    ) -> DataListView[AdminPlacePhotoView]:
        exists = await self._place_reader.exists(place_id=query.place_id)
        if not exists:
            raise PlaceNotFound(place_id=query.place_id)

        photos = await self._place_reader.get_admin_photos_by_id(
            place_id=query.place_id
        )

        # TODO: add more metadata to photos (e.g. is_main, order, etc.)
        # TODO: think about photos in statuses like "hidden", "deleted", etc.

        return DataListView.create(
            [
                AdminPlacePhotoView.from_read_model(
                    photo, storage_url_builder=self._storage_url_builder
                )
                for photo in photos
            ]
        )
