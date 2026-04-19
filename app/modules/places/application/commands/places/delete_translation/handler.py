from dataclasses import dataclass
from uuid import UUID

from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class DeletePlaceTranslationCommand:
    place_id: UUID
    language_code: LanguageEnum
