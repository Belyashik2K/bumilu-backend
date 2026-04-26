from dataclasses import asdict

from app.core.domain.value_objects.location import LocationVO
from app.core.enums import LanguageEnum
from app.modules.chat.application.interfaces.location_context_provider import (
    ILocationContextProvider,
    LocationContext,
)
from app.modules.places.application.interfaces.readers.place import IPlaceReader


class LocationContextProvider(ILocationContextProvider):
    def __init__(
        self,
        place_reader: IPlaceReader,
    ) -> None:
        self._place_reader = place_reader

    async def get_context(
        self,
        location: LocationVO,
        translation_language: LanguageEnum,
        radius_meters: int = 1000,
    ) -> LocationContext:
        places = await self._place_reader.get_cards_in_radius(
            latitude=location.latitude,
            longitude=location.longitude,
            radius_meters=radius_meters,
            translation_language=translation_language,
            limit=100,
        )
        return LocationContext(nearby_places=[asdict(place) for place in places])
