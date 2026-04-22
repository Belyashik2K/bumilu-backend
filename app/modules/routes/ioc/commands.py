from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.routes.application.commands.add_point.handler import (
    AddRoutePointCommandHandler,
)
from app.modules.routes.application.commands.change_status.handler import (
    ChangeRouteStatusCommandHandler,
)
from app.modules.routes.application.commands.create.handler import (
    CreateRouteCommandHandler,
)
from app.modules.routes.application.commands.create_translation.handler import (
    CreateRouteTranslationCommandHandler,
)
from app.modules.routes.application.commands.delete.handler import (
    DeleteRouteCommandHandler,
)
from app.modules.routes.application.commands.delete_translation.handler import (
    DeleteRouteTranslationCommandHandler,
)
from app.modules.routes.application.commands.remove_point.handler import (
    RemoveRoutePointCommandHandler,
)
from app.modules.routes.application.commands.replace_points.handler import (
    ReplaceRoutePointsCommandHandler,
)
from app.modules.routes.application.commands.update_translation.handler import (
    UpdateRouteTranslationCommandHandler,
)
from app.modules.routes.application.interfaces.repositories.route import (
    IRouteRepository,
)


class RoutesCommandHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def create_route_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> CreateRouteCommandHandler:
        return CreateRouteCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_route_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> DeleteRouteCommandHandler:
        return DeleteRouteCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def change_route_status_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
        place_repository: IPlaceRepository,
    ) -> ChangeRouteStatusCommandHandler:
        return ChangeRouteStatusCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
            place_repository=place_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def replace_route_points_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
        place_reader: IPlaceReader,
    ) -> ReplaceRoutePointsCommandHandler:
        return ReplaceRoutePointsCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def create_route_translation_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> CreateRouteTranslationCommandHandler:
        return CreateRouteTranslationCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def update_route_translation_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> UpdateRouteTranslationCommandHandler:
        return UpdateRouteTranslationCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_route_translation_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> DeleteRouteTranslationCommandHandler:
        return DeleteRouteTranslationCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def add_route_point_handler(
        self,
        transaction_manager: ITransactionManager,
        place_reader: IPlaceReader,
        route_repository: IRouteRepository,
    ) -> AddRoutePointCommandHandler:
        return AddRoutePointCommandHandler(
            transaction_manager=transaction_manager,
            place_reader=place_reader,
            route_repository=route_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def remove_route_point_handler(
        self,
        transaction_manager: ITransactionManager,
        route_repository: IRouteRepository,
    ) -> RemoveRoutePointCommandHandler:
        return RemoveRoutePointCommandHandler(
            transaction_manager=transaction_manager,
            route_repository=route_repository,
        )
