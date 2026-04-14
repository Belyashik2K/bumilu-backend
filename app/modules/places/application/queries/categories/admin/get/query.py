from dataclasses import dataclass
from uuid import UUID

from app.core.application.queries.language import LanguageMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminPlaceCategoryQuery(LanguageMixin):
    actor_id: UUID
    category_id: UUID
