from dataclasses import dataclass
from uuid import UUID

from app.core.application.queries.language import LanguageMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminPlaceQuery(LanguageMixin):
    place_id: UUID
