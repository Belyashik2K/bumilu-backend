from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import (
    PaginatedView,
)
from app.modules.places.shared.enums.route_sort import RouteSortByEnum
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.get_all.query import GetAllRoutesQuery
from app.modules.routes.application.queries.shared.models.route_card import (
    RouteCardReadModel,
)


class GetAllRoutesQueryHandler(
    IQueryHandler[GetAllRoutesQuery, PaginatedView[RouteCardReadModel]]
):
    def __init__(self, route_reader: IRouteReader) -> None:
        self._route_reader = route_reader

    async def handle(
        self, query: GetAllRoutesQuery
    ) -> PaginatedView[RouteCardReadModel]:
        latitude = query.latitude
        longitude = query.longitude
        sort_by = query.sort_by

        if not latitude or not longitude:
            latitude = None
            longitude = None
            sort_by = sort_by if sort_by != RouteSortByEnum.NEAREST else None

        routes_cards = await self._route_reader.get_all(
            translation_language=query.language,
            latitude=latitude,
            longitude=longitude,
            sort_by=sort_by,
            limit=query.limit,
            offset=query.offset,
        )

        return PaginatedView.create(
            items=routes_cards.items,
            total=routes_cards.total,
            limit=query.limit,
            offset=query.offset,
        )
