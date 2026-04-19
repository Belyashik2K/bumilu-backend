from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import RouteIdVO
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.routes.application.commands.change_status.command import (
    ChangeRouteStatusCommand,
)
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
    RouteLoadOptions,
)
from app.modules.routes.shared.enums.route_status import RouteStatusEnum


class ChangeRouteStatusCommandHandler(ICommandHandler[ChangeRouteStatusCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
        place_repository: IPlaceRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._route_repository = route_repository
        self._place_repository = place_repository

    async def handle(self, command: ChangeRouteStatusCommand) -> None:
        route_id = RouteIdVO.from_uuid(command.route_id)
        route = await self._route_repository.get_by_id(
            route_id, options=RouteLoadOptions(translations=True, points=True)
        )
        if route is None:
            raise RouteNotFound(route_id.value)

        if command.status == RouteStatusEnum.PUBLISHED:
            place_ids = [point.place_id for point in route.points]
            unpublished_place_ids = await self._place_repository.get_unpublished_ids(
                place_ids
            )
            route.publish(unpublished_place_ids=unpublished_place_ids)
        else:
            route.change_status(command.status)

        await self._route_repository.save(route)
