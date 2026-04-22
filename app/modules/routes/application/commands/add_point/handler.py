from app.core.application.commands import (
    ICommandHandler,
)
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    RouteIdVO,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.routes.application.commands.add_point.command import (
    AddRoutePointCommand,
)
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
    RouteLoadOptions,
)


class AddRoutePointCommandHandler(ICommandHandler[AddRoutePointCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_reader: IPlaceReader,
        route_repository: IRouteRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_reader = place_reader
        self._route_repository = route_repository

    async def handle(self, command: AddRoutePointCommand) -> None:
        route_id = RouteIdVO.from_uuid(command.route_id)
        route = await self._route_repository.get_by_id(
            route_id=route_id, options=RouteLoadOptions(points=True)
        )
        if route is None:
            raise RouteNotFound(route_id=route_id.value)

        exists = await self._place_reader.exists(
            place_id=command.place_id,
        )
        if not exists:
            raise PlaceNotFound(place_id=command.place_id)

        route.add_point(
            place_id=PlaceIdVO.from_uuid(command.place_id),
        )
        await self._route_repository.save(route)
