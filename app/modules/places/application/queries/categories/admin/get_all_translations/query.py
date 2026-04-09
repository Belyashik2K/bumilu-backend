from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminPlaceCategoryTranslationsListQuery:
    actor_id: UUID
    category_id: UUID
