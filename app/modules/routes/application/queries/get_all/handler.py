from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.shared.enums.route_sort import RouteSortByEnum
from app.modules.routes.application.queries.get_all.query import GetAllRoutesQuery
from app.modules.routes.application.queries.shared.readers.route import IRouteReader
from app.modules.routes.application.queries.shared.views import PaginatedRouteCardView


class GetAllRoutesQueryHandler(
    IQueryHandler[GetAllRoutesQuery, PaginatedRouteCardView]
):
    def __init__(self, route_reader: IRouteReader) -> None:
        self._route_reader = route_reader

    async def handle(self, query: GetAllRoutesQuery) -> PaginatedRouteCardView:
        if not query.latitude or not query.longitude:
            query.latitude = None
            query.longitude = None
            query.sort_by = RouteSortByEnum.NEW

        routes_cards = await self._route_reader.get_all(
            translation_language=query.language,
            latitude=query.latitude,
            longitude=query.longitude,
            sort_by=query.sort_by,
            limit=query.limit,
            offset=query.offset,
        )

        return PaginatedRouteCardView(
            routes=routes_cards.items,
            pagination=OffsetPagination.create(
                total=routes_cards.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
