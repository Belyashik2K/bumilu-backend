from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class DeletePlaceCategoryCommand:
    category_id: UUID
