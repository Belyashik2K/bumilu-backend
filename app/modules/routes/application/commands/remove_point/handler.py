from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    PlaceIdVO,
    RouteIdVO,
)
from app.modules.routes.application.commands.remove_point.command import (
    RemoveRoutePointCommand,
)
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
    RouteLoadOptions,
)


class RemoveRoutePointCommandHandler(ICommandHandler[RemoveRoutePointCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._route_repository = route_repository

    async def handle(self, command: RemoveRoutePointCommand) -> None:
        route_id = RouteIdVO.from_uuid(command.route_id)
        route = await self._route_repository.get_by_id(
            route_id=route_id,
            options=RouteLoadOptions(
                points=True,
            ),
        )
        if route is None:
            raise RouteNotFound(route_id=command.route_id)

        place_id = PlaceIdVO.from_uuid(command.place_id)

        route.remove_point(place_id=place_id)
        await self._route_repository.save(route)
