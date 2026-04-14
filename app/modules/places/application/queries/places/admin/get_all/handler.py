from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get_all.query import (
    GetAdminPlacesListQuery,
)
from app.modules.places.application.queries.places.admin.get_all.view import (
    PaginatedAdminPlacesView,
)


class GetAdminPlacesListQueryHandler(
    IQueryHandler[GetAdminPlacesListQuery, PaginatedAdminPlacesView]
):
    def __init__(self, place_reader: IPlaceReader) -> None:
        self._place_reader = place_reader

    async def handle(self, query: GetAdminPlacesListQuery) -> PaginatedAdminPlacesView:
        places = await self._place_reader.admin_get_all(
            title_like=query.title_like,
            category_slug=query.category_slug,
            limit=query.limit,
            offset=query.offset,
            optional_translation_language=query.language,
        )
        return PaginatedAdminPlacesView(
            data=places.items,
            pagination=OffsetPagination.create(
                total=places.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
