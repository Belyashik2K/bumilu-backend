from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.routes.application.interfaces.readers import IRouteReader
from app.modules.routes.application.queries.build_route_path.handler import (
    BuildRoutePathForRouteQueryHandler,
)
from app.modules.routes.application.queries.get.handler import GetRouteQueryHandler
from app.modules.routes.application.queries.get_all.handler import (
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
        self, route_reader: IRouteReader
    ) -> GetRouteQueryHandler:
        return GetRouteQueryHandler(
            route_reader=route_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def build_route_path_for_route_handler(
        self, route_reader: IRouteReader, routing_gateway: IRoutingGateway
    ) -> BuildRoutePathForRouteQueryHandler:
        return BuildRoutePathForRouteQueryHandler(
            route_reader=route_reader,
            routing_gateway=routing_gateway,
        )
