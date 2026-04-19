from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.application.commands.places.add_phone.command import (
    AddPlacePhoneCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
    PlaceLoadOptions,
)
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)


class AddPlacePhoneCommandHandler(ICommandHandler[AddPlacePhoneCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository

    async def handle(self, command: AddPlacePhoneCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(
            place_id,
            options=PlaceLoadOptions(
                phones=True,
            ),
        )
        if place is None:
            raise PlaceNotFound(place_id.value)

        number = PlacePhoneNumberVO(command.number)
        place.add_phone(
            number=number,
            type=command.type,
            is_primary=command.is_primary,
        )
        await self._place_repository.save(place)
