from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.favourites.application.interfaces.preview_provider import (
    IFavouritePreviewProvider,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum
from app.modules.places.application.queries.places.shared.models.place_card import (
    PlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)


class PlaceFavouritePreviewProvider(IFavouritePreviewProvider):
    supported_type = FavouriteEntityTypeEnum.PLACE

    def __init__(self, place_reader: IPlaceReader) -> None:
        self._place_reader = place_reader

    async def load_many(
        self, ids: list[UUID], translation_language: LanguageEnum
    ) -> dict[UUID, PlaceCardReadModel]:
        place_cards = await self._place_reader.get_cards_by_ids(
            ids, translation_language
        )

        return {card.id: card for card in place_cards}
