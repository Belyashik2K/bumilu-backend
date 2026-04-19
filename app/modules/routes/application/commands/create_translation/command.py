from dataclasses import dataclass
from uuid import UUID

from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateRouteTranslationCommand:
    route_id: UUID
    language_code: LanguageEnum
    title: str
    description: str
    short_description: str
