from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.constants import (
    UNSET,
    UnsetType,
)
from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceTranslationData:
    language_code: LanguageEnum
    title: str | UnsetType = field(default=UNSET)
    description: str | UnsetType = field(default=UNSET)
    short_description: str | UnsetType = field(default=UNSET)
    display_address: str | UnsetType = field(default=UNSET)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceTranslationCommand:
    place_id: UUID
    data: PlaceTranslationData
