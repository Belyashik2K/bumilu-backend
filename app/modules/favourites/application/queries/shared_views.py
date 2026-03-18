from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class FavouriteEntityInfoView:
    id: UUID
    type: FavouriteEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class FavouriteView:
    entity: FavouriteEntityInfoView
    created_at: datetime
