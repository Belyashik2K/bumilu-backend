from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhoneIdVO,
)
from app.modules.places.application.commands.places.make_phone_primary.command import (
    MakePlacePhonePrimaryCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)


class MakePlacePhonePrimaryCommandHandler(
    ICommandHandler[MakePlacePhonePrimaryCommand]
):
    def __init__(
        self,
        place_repository: IPlaceRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository

    async def handle(self, command: MakePlacePhonePrimaryCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id_with_phones(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        phone_id = PlacePhoneIdVO.from_uuid(command.phone_id)

        place.make_phone_primary(phone_id=phone_id)
        await self._place_repository.save(place)
