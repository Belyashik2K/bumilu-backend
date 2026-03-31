from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.routes.application.queries.get.handler import GetRouteQueryHandler
from app.modules.routes.application.queries.get_all.handler import (
    GetAllRoutesQueryHandler,
)
from app.modules.routes.application.queries.shared.readers.route import IRouteReader


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
