from dataclasses import dataclass
from uuid import UUID

from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminPlaceCategoryTranslationQuery:
    actor_id: UUID
    category_id: UUID
    language_code: LanguageEnum
