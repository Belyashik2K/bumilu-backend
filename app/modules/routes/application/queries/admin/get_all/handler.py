from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import PaginatedView
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.admin.get_all.query import (
    GetAdminRoutesListQuery,
)
from app.modules.routes.application.queries.shared.models.route_card import (
    AdminRouteCardReadModel,
)


class GetAdminRoutesListQueryHandler(
    IQueryHandler[GetAdminRoutesListQuery, PaginatedView[AdminRouteCardReadModel]]
):
    def __init__(
        self,
        route_reader: IRouteReader,
    ) -> None:
        self._route_reader = route_reader

    async def handle(
        self, query: GetAdminRoutesListQuery
    ) -> PaginatedView[AdminRouteCardReadModel]:
        data = await self._route_reader.admin_get_all(
            optional_translation_language=query.language,
            limit=query.limit,
            offset=query.offset,
        )

        return PaginatedView.create(
            items=data.items,
            limit=query.limit,
            offset=query.offset,
            total=data.total,
        )
