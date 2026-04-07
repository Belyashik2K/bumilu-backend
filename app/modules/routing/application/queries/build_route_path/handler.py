from app.core.application.queries import IQueryHandler
from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway
from app.modules.routing.application.models.route_path import RoutePath
from app.modules.routing.application.queries.build_route_path.query import (
    BuildRoutePathBetweenPointsQuery,
)


class BuildRoutePathBetweenPointsQueryHandler(
    IQueryHandler[BuildRoutePathBetweenPointsQuery, RoutePath]
):
    def __init__(self, routing_gateway: IRoutingGateway) -> None:
        self._routing_gateway = routing_gateway

    async def handle(self, query: BuildRoutePathBetweenPointsQuery) -> RoutePath:
        if len(query.points) < 2:
            raise ValueError("too few points for route")

        for previous_point, current_point in zip(
            query.points, query.points[1:], strict=False
        ):
            if current_point == previous_point:
                raise ValueError("consecutive points must be different")

        return await self._routing_gateway.get_route(
            points=query.points,
            mode=query.travel_mode,
            translation_language=query.language,
        )
