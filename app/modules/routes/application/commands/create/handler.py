from app.core.application.commands import (
    ICommandHandlerWithResult,
)
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.routes.application.commands.create.command import (
    CreateRouteCommand,
    CreateRouteCommandResult,
)
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
)
from app.modules.routes.domain.models.route.model import Route


class CreateRouteCommandHandler(
    ICommandHandlerWithResult[CreateRouteCommand, CreateRouteCommandResult]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._route_repository = route_repository

    async def handle(
        self,
        command: CreateRouteCommand,
    ) -> CreateRouteCommandResult:
        route = Route.create()

        await self._route_repository.save(route)

        return CreateRouteCommandResult(route_id=route.id.value)
