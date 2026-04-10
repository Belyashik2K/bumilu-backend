from dataclasses import dataclass
from uuid import UUID

from app.modules.places.shared.enums.place_category_status import (
    PlaceCategoryStatusEnum,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangePlaceCategoryStatusCommand:
    category_id: UUID
    status: PlaceCategoryStatusEnum
