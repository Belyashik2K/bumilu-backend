from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.core.domain.value_objects.location import LocationVO
from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class LocationContext:
    nearby_places: list[dict]


class ILocationContextProvider(ABC):
    @abstractmethod
    async def get_context(
        self,
        location: LocationVO,
        translation_language: LanguageEnum,
        radius_meters: int = 1000,
    ) -> LocationContext: ...
