from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhotoIdVO,
)
from app.modules.places.application.commands.places.start_photo_upload.command import (
    StartPlacePhotoUploadCommand,
    StartPlacePhotoUploadCommandResult,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.file_key_generator import (
    IFileKeyGenerator,
)
from app.modules.places.application.interfaces.file_storage import IFileStorage
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)


class StartPlacePhotoUploadCommandHandler(
    ICommandHandlerWithResult[
        StartPlacePhotoUploadCommand, StartPlacePhotoUploadCommandResult
    ]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        file_key_generator: IFileKeyGenerator,
        file_storage: IFileStorage,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository
        self._file_key_generator = file_key_generator
        self._file_storage = file_storage

    async def handle(
        self, command: StartPlacePhotoUploadCommand
    ) -> StartPlacePhotoUploadCommandResult:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        photo_id = PlacePhotoIdVO.new()

        file_key = self._file_key_generator.generate_place_photo_key(
            place_id=place.id,
            photo_id=photo_id,
            content_type=command.content_type,
        )
        photo = place.add_photo(
            photo_id=photo_id,
            file_key=file_key,
        )
        await self._place_repository.save(place)

        upload_url = await self._file_storage.generate_upload_url(
            file_key=file_key,
            content_type=command.content_type,
        )

        return StartPlacePhotoUploadCommandResult(
            photo_id=photo.id.value,
            file_key=file_key,
            upload_url=upload_url,
        )
