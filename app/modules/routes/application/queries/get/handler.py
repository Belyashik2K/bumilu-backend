from app.core.application.queries import IQueryHandler
from app.modules.routes.application.queries.get.query import GetRouteQuery
from app.modules.routes.application.queries.shared.readers.route import IRouteReader
from app.modules.routes.application.queries.shared.views import RouteView


class GetRouteQueryHandler(IQueryHandler[GetRouteQuery, RouteView]):
    def __init__(
        self,
        route_reader: IRouteReader,
    ) -> None:
        self._route_reader = route_reader

    async def handle(self, query: GetRouteQuery) -> RouteView:
        route = await self._route_reader.get_by_id(
            route_id=query.route_id,
            translation_language=query.language,
        )
        if not route:
            raise ValueError("Route not found")
        return route
