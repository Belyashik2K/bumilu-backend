from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import RouteIdVO
from app.modules.routes.application.commands.delete.command import DeleteRouteCommand
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
)


class DeleteRouteCommandHandler(ICommandHandler[DeleteRouteCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._route_repository = route_repository

    async def handle(self, command: DeleteRouteCommand) -> None:
        route_id = RouteIdVO.from_uuid(command.route_id)

        route = await self._route_repository.get_by_id(route_id)
        if route is None:
            raise RouteNotFound(route_id.value)

        await self._route_repository.delete_by_id(route.id)
