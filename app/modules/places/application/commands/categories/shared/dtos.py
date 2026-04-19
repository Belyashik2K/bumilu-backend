from dataclasses import dataclass

from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class NewPlaceCategoryTranslation:
    language_code: LanguageEnum
    name: str
