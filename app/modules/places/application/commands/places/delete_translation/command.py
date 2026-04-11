from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.application.commands.places.delete_translation.handler import (
    DeletePlaceTranslationCommand,
)
from app.modules.places.application.exceptions.place import (
    PlaceNotFound,
    PlaceTranslationNotFound,
)
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.application.interfaces.repositories.place_translation import (
    IPlaceTranslationRepository,
)


class DeletePlaceTranslationCommandHandler(
    ICommandHandler[DeletePlaceTranslationCommand]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_translation_repository: IPlaceTranslationRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository
        self._place_translation_repository = place_translation_repository

    async def handle(self, command: DeletePlaceTranslationCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        translation = (
            await self._place_translation_repository.get_by_place_id_and_language_code(
                place_id=place_id,
                language_code=command.language_code,
            )
        )
        if translation is None:
            raise PlaceTranslationNotFound(
                place_id=place_id.value,
                language_code=command.language_code,
            )

        place.remove_translation(command.language_code)

        await self._place_translation_repository.delete_by_id(translation.id)
        await self._place_repository.save(place)
