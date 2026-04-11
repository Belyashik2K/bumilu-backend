from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceTranslationData:
    language_code: LanguageEnum
    title: str
    description: str
    short_description: str
    display_address: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceTranslationCommand:
    place_id: UUID
    data: PlaceTranslationData
