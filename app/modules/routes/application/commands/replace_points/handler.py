from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    RouteIdVO,
)
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.routes.application.commands.replace_points.command import (
    ReplaceRoutePointsCommand,
)
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
    RouteLoadOptions,
)


class ReplaceRoutePointsCommandHandler(ICommandHandler[ReplaceRoutePointsCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
        place_reader: IPlaceReader,
    ) -> None:
        super().__init__(transaction_manager)
        self._route_repository = route_repository
        self._place_reader = place_reader

    async def handle(self, command: ReplaceRoutePointsCommand) -> None:
        route_id = RouteIdVO.from_uuid(command.route_id)
        route = await self._route_repository.get_by_id(
            route_id, options=RouteLoadOptions(points=True)
        )
        if route is None:
            raise RouteNotFound(route_id.value)

        expected_existing_places_count = len(command.place_ids)
        actual_existing_places_count = await self._place_reader.count_existing_places(
            place_ids=command.place_ids
        )

        if expected_existing_places_count != actual_existing_places_count:
            raise ValueError(
                f"Some of the provided place IDs do not exist. Expected {expected_existing_places_count}, "
                f"but found {actual_existing_places_count}."
            )

        route.replace_points(
            [PlaceIdVO.from_uuid(place_id) for place_id in command.place_ids]
        )
        await self._route_repository.save(route)
