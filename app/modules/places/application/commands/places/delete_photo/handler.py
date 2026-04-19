from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhotoIdVO,
)
from app.modules.places.application.commands.places.delete_photo.command import (
    DeletePlacePhotoCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.file_storage import IFileStorage
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
    PlaceLoadOptions,
)


class DeletePlacePhotoCommandHandler(ICommandHandler[DeletePlacePhotoCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        file_storage: IFileStorage,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository
        self._file_storage = file_storage

    async def handle(
        self,
        command: DeletePlacePhotoCommand,
    ) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        photo_id = PlacePhotoIdVO.from_uuid(command.photo_id)

        place = await self._place_repository.get_by_id(
            place_id,
            options=PlaceLoadOptions(photos=True),
        )
        if place is None:
            raise PlaceNotFound(place_id.value)

        photo = place.get_photo(photo_id=photo_id)

        file_key = photo.file_key
        thumbnail_file_key = photo.thumbnail_file_key

        place.remove_photo(photo_id=photo_id)

        await self._place_repository.save(place)

        try:
            # TODO: to workers
            await self._file_storage.delete_object(file_key=file_key)

            if thumbnail_file_key:
                await self._file_storage.delete_object(file_key=thumbnail_file_key)
        except Exception as e:
            print(f"Error deleting files from storage: {e}")
            # TODO: log error
            pass
