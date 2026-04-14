from dataclasses import (
    dataclass,
)

from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceTranslationReadModel:
    language_code: LanguageEnum
    title: str
    description: str
    short_description: str
    display_address: str
