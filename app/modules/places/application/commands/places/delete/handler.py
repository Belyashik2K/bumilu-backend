from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.application.commands.places.delete.command import (
    DeletePlaceCommand,
)
from app.modules.places.application.exceptions.place import (
    PlaceIsUsedInRoute,
    PlaceNotFound,
)
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.routes.application.interfaces.readers.route import IRouteReader


class DeletePlaceCommandHandler(ICommandHandler[DeletePlaceCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        route_reader: IRouteReader,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository
        self._route_reader = route_reader

    async def handle(self, command: DeletePlaceCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id=place_id.value)

        routes_count = await self._route_reader.count_by_place_id(place_id.value)
        if routes_count != 0:
            raise PlaceIsUsedInRoute(
                place_id=place_id.value,
                routes_count=routes_count,
            )

        await self._place_repository.delete_by_id(place.id)
