from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway
from app.modules.routing.application.queries.get_route.handler import (
    GetRouteBetweenPointsQueryHandler,
)


class RoutingQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_route_between_points_handler(
        self,
        routing_gateway: IRoutingGateway,
    ) -> GetRouteBetweenPointsQueryHandler:
        return GetRouteBetweenPointsQueryHandler(routing_gateway=routing_gateway)
