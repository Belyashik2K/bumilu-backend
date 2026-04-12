from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhotoIdVO,
)
from app.modules.places.application.commands.places.complete_photo_upload.command import (
    CompletePlacePhotoUploadCommand,
)
from app.modules.places.application.exceptions.place import (
    PlaceNotFound,
    PlacePhotoFileNotUploaded,
)
from app.modules.places.application.interfaces.file_storage import IFileStorage
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)


class CompletePlacePhotoUploadCommandHandler(
    ICommandHandler[CompletePlacePhotoUploadCommand]
):
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
        command: CompletePlacePhotoUploadCommand,
    ) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        photo_id = PlacePhotoIdVO.from_uuid(command.photo_id)

        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        photo = place.get_photo(photo_id=photo_id)
        object_info = await self._file_storage.get_object_info(
            file_key=photo.file_key,
        )
        if object_info is None:
            raise PlacePhotoFileNotUploaded(
                place_id=place.id.value,
                photo_id=photo.id.value,
                file_key=photo.file_key,
            )

        place.mark_photo_uploaded(photo_id=photo_id)
        await self._place_repository.save(place)
