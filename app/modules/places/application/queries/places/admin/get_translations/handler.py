from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.interfaces.readers.place_translation import (
    IPlaceTranslationReader,
)
from app.modules.places.application.queries.places.admin.get_translations.query import (
    GetAdminPlaceTranslationsQuery,
)
from app.modules.places.application.queries.places.admin.get_translations.view import (
    PaginatedAdminPlaceTranslationsView,
)


class GetAdminPlaceTranslationsQueryHandler(
    IQueryHandler[
        GetAdminPlaceTranslationsQuery,
        PaginatedAdminPlaceTranslationsView,
    ]
):
    def __init__(
        self,
        place_translation_reader: IPlaceTranslationReader,
    ) -> None:
        self._place_translation_reader = place_translation_reader

    async def handle(
        self, query: GetAdminPlaceTranslationsQuery
    ) -> PaginatedAdminPlaceTranslationsView:
        translations = await self._place_translation_reader.list_by_place_id(
            place_id=query.place_id,
            offset=query.offset,
            limit=query.limit,
        )

        return PaginatedAdminPlaceTranslationsView(
            data=translations.items,
            pagination=OffsetPagination.create(
                total=translations.total,
                offset=query.offset,
                limit=query.limit,
            ),
        )
