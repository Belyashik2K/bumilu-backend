from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdatePlaceCategoryTranslationCommand:
    category_id: UUID
    language_code: LanguageEnum
    name: str | None = field(default=None)
