from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import PaginatedView
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.interfaces.readers.route_translation import (
    IRouteTranslationReader,
)
from app.modules.routes.application.queries.admin.get_translations.query import (
    GetAdminRouteTranslationsQuery,
)
from app.modules.routes.application.queries.shared.models.route_translation import (
    RouteTranslationReadModel,
)


class GetAdminRouteTranslationsQueryHandler(
    IQueryHandler[
        GetAdminRouteTranslationsQuery, PaginatedView[RouteTranslationReadModel]
    ]
):
    def __init__(
        self,
        route_reader: IRouteReader,
        route_translation_reader: IRouteTranslationReader,
    ) -> None:
        self._route_reader = route_reader
        self._route_translation_reader = route_translation_reader

    async def handle(
        self, query: GetAdminRouteTranslationsQuery
    ) -> PaginatedView[RouteTranslationReadModel]:
        exists = await self._route_reader.exists(
            route_id=query.route_id,
        )
        if not exists:
            raise RouteNotFound(route_id=query.route_id)

        translations = await self._route_translation_reader.list_by_route_id(
            route_id=query.route_id,
            limit=query.limit,
            offset=query.offset,
        )

        return PaginatedView.create(
            items=translations.items,
            limit=query.limit,
            offset=query.offset,
            total=translations.total,
        )
