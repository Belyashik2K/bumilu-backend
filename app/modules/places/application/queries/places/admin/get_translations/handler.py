from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import (
    PaginatedView,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.readers.place_translation import (
    IPlaceTranslationReader,
)
from app.modules.places.application.queries.places.admin.get_translations.query import (
    GetAdminPlaceTranslationsQuery,
)
from app.modules.places.application.queries.places.shared.models.place_translation import (
    PlaceTranslationReadModel,
)


class GetAdminPlaceTranslationsQueryHandler(
    IQueryHandler[
        GetAdminPlaceTranslationsQuery, PaginatedView[PlaceTranslationReadModel]
    ]
):
    def __init__(
        self,
        place_reader: IPlaceReader,
        place_translation_reader: IPlaceTranslationReader,
    ) -> None:
        self._place_reader = place_reader
        self._place_translation_reader = place_translation_reader

    async def handle(
        self, query: GetAdminPlaceTranslationsQuery
    ) -> PaginatedView[PlaceTranslationReadModel]:
        exists = await self._place_reader.exists(place_id=query.place_id)
        if not exists:
            raise PlaceNotFound(place_id=query.place_id)

        translations = await self._place_translation_reader.list_by_place_id(
            place_id=query.place_id,
            offset=query.offset,
            limit=query.limit,
        )

        return PaginatedView.create(
            items=translations.items,
            total=translations.total,
            offset=query.offset,
            limit=query.limit,
        )
