from app.core.application.queries import IQueryHandler
from app.modules.routes.application.exceptions.route import (
    RouteHasTooFewPointsForBuildingRoutePath,
    RouteNotFound,
)
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.admin.build_route_path.query import (
    BuildAdminRoutePathForRouteQuery,
)
from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway
from app.modules.routing.application.models.route_path import RoutePath
from app.modules.routing.application.queries.build_route_path.query import Waypoint


class BuildAdminRoutePathForRouteQueryHandler(
    IQueryHandler[BuildAdminRoutePathForRouteQuery, RoutePath]
):
    def __init__(
        self,
        route_reader: IRouteReader,
        routing_gateway: IRoutingGateway,
    ) -> None:
        self._routing_gateway = routing_gateway
        self._route_reader = route_reader

    async def handle(self, query: BuildAdminRoutePathForRouteQuery) -> RoutePath:
        exists = await self._route_reader.exists(route_id=query.route_id)
        if not exists:
            raise RouteNotFound(route_id=query.route_id)

        waypoints = await self._route_reader.get_route_waypoints(
            route_id=query.route_id
        )

        if len(waypoints) < 2:
            raise RouteHasTooFewPointsForBuildingRoutePath(route_id=query.route_id)

        return await self._routing_gateway.get_route(
            points=[
                Waypoint(latitude=point.latitude, longitude=point.longitude)
                for point in sorted(waypoints, key=lambda p: p.index)
            ],
            mode=query.travel_mode,
            translation_language=query.language,
        )
