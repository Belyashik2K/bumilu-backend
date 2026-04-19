from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import DataListView
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.admin.get_points.query import (
    GetAdminRoutePointsQuery,
)
from app.modules.routes.application.queries.shared.models.route_point import (
    AdminRoutePointReadModel,
)


class GetAdminRoutePointsQueryHandler(
    IQueryHandler[GetAdminRoutePointsQuery, DataListView[AdminRoutePointReadModel]]
):
    def __init__(
        self, route_reader: IRouteReader, storage_url_builder: IFileStorageURLBuilder
    ) -> None:
        self._route_reader = route_reader
        self._storage_url_builder = storage_url_builder

    async def handle(
        self, query: GetAdminRoutePointsQuery
    ) -> DataListView[AdminRoutePointReadModel]:
        points = await self._route_reader.get_admin_route_points(
            route_id=query.route_id, optional_translation_language=query.language
        )
        return DataListView.create(points)
