from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.application.commands.places.create_translation.command import (
    CreatePlaceTranslationCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.application.interfaces.repositories.place_translation import (
    IPlaceTranslationRepository,
)
from app.modules.places.domain.places.models.place_translation.model import (
    PlaceTranslationData,
)
from app.modules.places.domain.places.value_objects.description.object import (
    PlaceDescriptionVO,
)
from app.modules.places.domain.places.value_objects.display_address.object import (
    PlaceDisplayAddressVO,
)
from app.modules.places.domain.places.value_objects.short_description.object import (
    PlaceShortDescriptionVO,
)
from app.modules.places.domain.places.value_objects.title.object import PlaceTitleVO


class CreatePlaceTranslationCommandHandler(
    ICommandHandler[CreatePlaceTranslationCommand]
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

    async def handle(self, command: CreatePlaceTranslationCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        translation_data = PlaceTranslationData(
            language_code=command.data.language_code,
            title=PlaceTitleVO(command.data.title),
            description=PlaceDescriptionVO(command.data.description),
            short_description=PlaceShortDescriptionVO(command.data.short_description),
            display_address=PlaceDisplayAddressVO(command.data.display_address),
        )
        new_translation = place.create_translation(translation_data)

        await self._place_translation_repository.save(
            new_translation
        )  # TODO: remove _place_translation_repository and save translation through place repository
        await self._place_repository.save(place)
