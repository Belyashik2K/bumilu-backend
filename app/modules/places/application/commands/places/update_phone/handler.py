from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.constants import is_unset
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhoneIdVO,
)
from app.modules.places.application.commands.places.update_phone.command import (
    UpdatePlacePhoneCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
    PlaceLoadOptions,
)
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)


class UpdatePlacePhoneCommandHandler(ICommandHandler[UpdatePlacePhoneCommand]):
    def __init__(
        self,
        place_repository: IPlaceRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository

    async def handle(self, command: UpdatePlacePhoneCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(
            place_id,
            options=PlaceLoadOptions(
                phones=True,
            ),
        )
        if place is None:
            raise PlaceNotFound(place_id.value)

        phone_id = PlacePhoneIdVO.from_uuid(command.phone_id)

        new_number = (
            PlacePhoneNumberVO(command.number)
            if not is_unset(command.number)  # TODO: use it in other places
            else None
        )
        new_type = command.type if not is_unset(command.type) else None

        place.update_phone(
            phone_id=phone_id,
            number=new_number,
            type=new_type,
        )
        await self._place_repository.save(place)
