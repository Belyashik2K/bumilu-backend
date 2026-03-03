from dataclasses import dataclass
from uuid import UUID

from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class FavouriteItemDTO:
    entity_type: FavouriteEntityTypeEnum
    entity_id: UUID
