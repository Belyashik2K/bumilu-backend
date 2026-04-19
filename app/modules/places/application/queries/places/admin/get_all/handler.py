from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import PaginatedView
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get_all.query import (
    GetAdminPlacesListQuery,
)
from app.modules.places.application.queries.places.shared.models.place_card import (
    AdminPlaceCardReadModel,
)


class GetAdminPlacesListQueryHandler(
    IQueryHandler[GetAdminPlacesListQuery, PaginatedView[AdminPlaceCardReadModel]]
):
    def __init__(self, place_reader: IPlaceReader) -> None:
        self._place_reader = place_reader

    async def handle(
        self, query: GetAdminPlacesListQuery
    ) -> PaginatedView[AdminPlaceCardReadModel]:
        places = await self._place_reader.admin_get_all(
            title_like=query.title_like,
            category_slug=query.category_slug,
            limit=query.limit,
            offset=query.offset,
            optional_translation_language=query.language,
        )
        return PaginatedView.create(
            items=places.items,
            limit=query.limit,
            offset=query.offset,
            total=places.total,
        )
