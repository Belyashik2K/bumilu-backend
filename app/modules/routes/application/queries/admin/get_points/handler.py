from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import DataListView
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.queries.places.shared.views import PlaceCardView
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.admin.get_points.query import (
    GetAdminRoutePointsQuery,
)
from app.modules.routes.application.queries.shared.views import RoutePointView


class GetAdminRoutePointsQueryHandler(
    IQueryHandler[GetAdminRoutePointsQuery, DataListView[RoutePointView]]
):
    def __init__(
        self, route_reader: IRouteReader, storage_url_builder: IFileStorageURLBuilder
    ) -> None:
        self._route_reader = route_reader
        self._storage_url_builder = storage_url_builder

    async def handle(
        self, query: GetAdminRoutePointsQuery
    ) -> DataListView[RoutePointView]:
        points = await self._route_reader.get_route_points(route_id=query.route_id)

        return DataListView.create(
            [
                RoutePointView(
                    index=point.index,
                    preview=PlaceCardView.from_read_model(
                        point.preview, storage_url_builder=self._storage_url_builder
                    ),
                )
                for point in sorted(points, key=lambda p: p.index)
            ]
        )
