from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.favourites.application.shared.dtos import FavouriteItemDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllFavouritesByUserQuery:
    actor_id: UUID
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllFavouritesByUserQueryResult:
    user_id: UUID
    items: list[FavouriteItemDTO] = field(default_factory=list)
