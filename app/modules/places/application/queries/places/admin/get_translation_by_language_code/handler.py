from app.core.application.queries import IQueryHandler
from app.modules.places.application.exceptions.place import (
    PlaceNotFound,
    PlaceTranslationNotFound,
)
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.readers.place_translation import (
    IPlaceTranslationReader,
)
from app.modules.places.application.queries.places.admin.get_translation_by_language_code.query import (
    GetAdminPlaceTranslationByLanguageCodeQuery,
)
from app.modules.places.application.queries.places.shared.models.place_translation import (
    PlaceTranslationReadModel,
)


class GetAdminPlaceTranslationByLanguageCodeQueryHandler(
    IQueryHandler[
        GetAdminPlaceTranslationByLanguageCodeQuery,
        PlaceTranslationReadModel,
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
        self, query: GetAdminPlaceTranslationByLanguageCodeQuery
    ) -> PlaceTranslationReadModel:
        exists = await self._place_reader.exists(place_id=query.place_id)
        if not exists:
            raise PlaceNotFound(place_id=query.place_id)

        place_translation = (
            await self._place_translation_reader.get_by_place_id_and_language_code(
                place_id=query.place_id, language_code=query.language_code
            )
        )
        if place_translation is None:
            raise PlaceTranslationNotFound(
                place_id=query.place_id, language_code=query.language_code
            )

        return place_translation
