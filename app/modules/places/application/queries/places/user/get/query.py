from dataclasses import dataclass
from uuid import UUID

from app.core.application.queries.language import LanguageMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class GetPlaceQuery(LanguageMixin):
    place_id: UUID
    actor_id: UUID
