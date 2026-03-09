from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class FavouriteEntityView:
    entity_type: FavouriteEntityTypeEnum
    entity_id: UUID
    created_at: datetime
