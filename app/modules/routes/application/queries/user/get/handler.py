from app.core.application.queries import IQueryHandler
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.queries.places.shared.views import PlaceCardView
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.shared.views import (
    RoutePointView,
    RouteView,
)
from app.modules.routes.application.queries.user.get.query import GetRouteQuery


class GetRouteQueryHandler(IQueryHandler[GetRouteQuery, RouteView]):
    def __init__(
        self,
        route_reader: IRouteReader,
        storage_url_builder: IFileStorageURLBuilder,
    ) -> None:
        self._route_reader = route_reader
        self._storage_url_builder = storage_url_builder

    async def handle(self, query: GetRouteQuery) -> RouteView:
        route = await self._route_reader.get_by_id(
            route_id=query.route_id,
            translation_language=query.language,
        )
        if not route:
            raise RouteNotFound(route_id=query.route_id)

        return RouteView(
            id=route.id,
            title=route.title,
            description=route.description,
            short_description=route.short_description,
            points=[
                RoutePointView(
                    index=point.index,
                    preview=PlaceCardView.from_read_model(
                        point.preview, storage_url_builder=self._storage_url_builder
                    ),
                )
                for point in sorted(route.points, key=lambda p: p.index)
            ],
            total_points=route.total_points,
        )
