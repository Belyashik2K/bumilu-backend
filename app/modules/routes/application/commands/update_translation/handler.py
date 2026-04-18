from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.constants import (
    is_unset,
)
from app.core.domain.value_objects.id import RouteIdVO
from app.modules.routes.application.commands.update_translation.command import (
    UpdateRouteTranslationCommand,
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


class UpdateRouteTranslationCommandHandler(
    ICommandHandler[UpdateRouteTranslationCommand]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._route_repository = route_repository

    async def handle(self, command: UpdateRouteTranslationCommand) -> None:
        route_id = RouteIdVO.from_uuid(command.route_id)
        route = await self._route_repository.get_by_id(
            route_id, options=RouteLoadOptions(translations=True)
        )
        if route is None:
            raise RouteNotFound(route_id.value)

        new_title = RouteTitleVO(command.title) if not is_unset(command.title) else None
        new_description = (
            RouteDescriptionVO(command.description)
            if not is_unset(command.description)
            else None
        )
        new_short_description = (
            RouteShortDescriptionVO(command.short_description)
            if not is_unset(command.short_description)
            else None
        )

        route.update_translation(
            language_code=command.language_code,
            title=new_title,
            description=new_description,
            short_description=new_short_description,
        )

        await self._route_repository.save(route)
