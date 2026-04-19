from app.core.application.queries import IQueryHandler
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.admin.get.query import GetAdminRouteQuery
from app.modules.routes.application.queries.shared.models.route_details import (
    AdminRouteDetailsReadModel,
)


class GetAdminRouteQueryHandler(
    IQueryHandler[GetAdminRouteQuery, AdminRouteDetailsReadModel]
):
    def __init__(
        self,
        route_reader: IRouteReader,
    ) -> None:
        self._route_reader = route_reader

    async def handle(self, query: GetAdminRouteQuery) -> AdminRouteDetailsReadModel:
        route = await self._route_reader.get_admin_by_id(
            route_id=query.route_id,
            optional_translation_language=query.language,
        )
        if route is None:
            raise RouteNotFound(route_id=query.route_id)
        return route
