from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.constants import UnsetType
from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.application.commands.places.update_translation.command import (
    UpdatePlaceTranslationCommand,
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


class UpdatePlaceTranslationCommandHandler(
    ICommandHandler[UpdatePlaceTranslationCommand]
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

    async def handle(
        self,
        command: UpdatePlaceTranslationCommand,
    ) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        place_translation = (
            await self._place_translation_repository.get_by_place_id_and_language_code(
                place_id=place_id,
                language_code=command.data.language_code,
            )
        )
        if place_translation is None:
            raise PlaceTranslationNotFound(
                place_id=place_id.value,
                language_code=command.data.language_code,
            )

        new_title = (
            PlaceTitleVO(command.data.title)
            if not isinstance(command.data.title, UnsetType)
            else place_translation.data.title
        )
        new_description = (
            PlaceDescriptionVO(command.data.description)
            if not isinstance(command.data.description, UnsetType)
            else place_translation.data.description
        )
        new_short_description = (
            PlaceShortDescriptionVO(command.data.short_description)
            if not isinstance(command.data.short_description, UnsetType)
            else place_translation.data.short_description
        )
        new_display_address = (
            PlaceDisplayAddressVO(command.data.display_address)
            if not isinstance(command.data.display_address, UnsetType)
            else place_translation.data.display_address
        )

        place_translation.update(
            title=new_title,
            description=new_description,
            short_description=new_short_description,
            display_address=new_display_address,
        )

        await self._place_translation_repository.save(place_translation)
