from app.core.application.queries import IQueryHandler
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.readers import IRouteReader
from app.modules.routes.application.queries.build_route_path.query import (
    BuildRoutePathForRouteQuery,
)
from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway
from app.modules.routing.application.models.route_path import RoutePath
from app.modules.routing.application.queries.build_route_path.query import Waypoint


class BuildRoutePathForRouteQueryHandler(
    IQueryHandler[BuildRoutePathForRouteQuery, RoutePath]
):
    def __init__(
        self,
        route_reader: IRouteReader,
        routing_gateway: IRoutingGateway,
    ) -> None:
        self._routing_gateway = routing_gateway
        self._route_reader = route_reader

    async def handle(self, query: BuildRoutePathForRouteQuery) -> RoutePath:
        route = await self._route_reader.get_by_id(
            route_id=query.route_id,
            translation_language=query.language,
        )
        if route is None:
            raise RouteNotFound(route_id=query.route_id)

        points = await self._route_reader.get_route_points(route_id=query.route_id)

        return await self._routing_gateway.get_route(
            points=[
                Waypoint(latitude=point.latitude, longitude=point.longitude)
                for point in sorted(points, key=lambda p: p.index)
            ],
            mode=query.travel_mode,
            translation_language=query.language,
        )
