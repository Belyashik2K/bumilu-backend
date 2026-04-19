from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import RouteIdVO
from app.modules.routes.application.commands.create_translation.command import (
    CreateRouteTranslationCommand,
)
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
    RouteLoadOptions,
)
from app.modules.routes.domain.value_objects.description.object import (
    RouteDescriptionVO,
)
from app.modules.routes.domain.value_objects.short_description.object import (
    RouteShortDescriptionVO,
)
from app.modules.routes.domain.value_objects.title.object import RouteTitleVO


class CreateRouteTranslationCommandHandler(
    ICommandHandler[CreateRouteTranslationCommand]
):
    def __init__(
        self,
        route_repository: IRouteRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._route_repository = route_repository

    async def handle(self, command: CreateRouteTranslationCommand) -> None:
        route_id = RouteIdVO.from_uuid(command.route_id)
        route = await self._route_repository.get_by_id(
            route_id, options=RouteLoadOptions(translations=True)
        )
        if route is None:
            raise RouteNotFound(route_id.value)

        route.add_translation(
            language_code=command.language_code,
            title=RouteTitleVO(command.title),
            short_description=RouteShortDescriptionVO(command.short_description),
            description=RouteDescriptionVO(command.description),
        )

        await self._route_repository.save(route)
