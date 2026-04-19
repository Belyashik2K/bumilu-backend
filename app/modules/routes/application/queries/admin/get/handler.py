from app.core.application.queries import IQueryHandler
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.admin.get.query import GetAdminRouteQuery


class GetAdminRouteQueryHandler(IQueryHandler[GetAdminRouteQuery, None]):
    def __init__(
        self,
        route_reader: IRouteReader,
    ) -> None:
        self._route_reader = route_reader

    async def handle(self, query: GetAdminRouteQuery) -> None:
        return None
