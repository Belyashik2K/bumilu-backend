from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhoneIdVO,
)
from app.modules.places.application.commands.places.delete_phone.command import (
    DeletePlacePhoneCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)


class DeletePlacePhoneCommandHandler(ICommandHandler[DeletePlacePhoneCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository

    async def handle(self, command: DeletePlacePhoneCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        phone_id = PlacePhoneIdVO.from_uuid(command.phone_id)

        place.remove_phone(phone_id=phone_id)

        await self._place_repository.save(place)
