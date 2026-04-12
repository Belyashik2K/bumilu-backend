from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.favourites.application.interfaces.preview_provider import (
    IFavouritePreviewProvider,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import PlaceCardView


class PlaceFavouritePreviewProvider(IFavouritePreviewProvider):
    supported_type = FavouriteEntityTypeEnum.PLACE

    def __init__(
        self, place_reader: IPlaceReader, storage_url_builder: IFileStorageURLBuilder
    ) -> None:
        self._place_reader = place_reader
        self._storage_url_builder = storage_url_builder

    async def load_many(
        self, ids: list[UUID], translation_language: LanguageEnum
    ) -> dict[UUID, PlaceCardView]:
        place_cards = await self._place_reader.get_cards_by_ids(
            ids, translation_language
        )

        return {
            card.id: PlaceCardView.from_read_model(
                card, storage_url_builder=self._storage_url_builder
            )
            for card in place_cards
        }
