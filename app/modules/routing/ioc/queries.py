from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway
from app.modules.routing.application.queries.build_route_path.handler import (
    BuildRoutePathBetweenPointsQueryHandler,
)


class RoutingQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_route_between_points_handler(
        self,
        routing_gateway: IRoutingGateway,
    ) -> BuildRoutePathBetweenPointsQueryHandler:
        return BuildRoutePathBetweenPointsQueryHandler(routing_gateway=routing_gateway)
