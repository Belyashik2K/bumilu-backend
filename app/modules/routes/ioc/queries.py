from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.admin.get_points.handler import (
    GetAdminRoutePointsQueryHandler,
)
from app.modules.routes.application.queries.user.build_route_path.handler import (
    BuildRoutePathForRouteQueryHandler,
)
from app.modules.routes.application.queries.user.get.handler import GetRouteQueryHandler
from app.modules.routes.application.queries.user.get_all.handler import (
    GetAllRoutesQueryHandler,
)
from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway


class RoutesQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_all_routes_handler(
        self, route_reader: IRouteReader
    ) -> GetAllRoutesQueryHandler:
        return GetAllRoutesQueryHandler(
            route_reader=route_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_route_handler(
        self, route_reader: IRouteReader, storage_url_builder: IFileStorageURLBuilder
    ) -> GetRouteQueryHandler:
        return GetRouteQueryHandler(
            route_reader=route_reader,
            storage_url_builder=storage_url_builder,
        )

    @provide(scope=Scope.REQUEST)
    async def build_route_path_for_route_handler(
        self, route_reader: IRouteReader, routing_gateway: IRoutingGateway
    ) -> BuildRoutePathForRouteQueryHandler:
        return BuildRoutePathForRouteQueryHandler(
            route_reader=route_reader,
            routing_gateway=routing_gateway,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_route_points_handler(
        self, route_reader: IRouteReader, storage_url_builder: IFileStorageURLBuilder
    ) -> GetAdminRoutePointsQueryHandler:
        return GetAdminRoutePointsQueryHandler(
            route_reader=route_reader,
            storage_url_builder=storage_url_builder,
        )
