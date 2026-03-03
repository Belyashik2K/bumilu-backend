from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.favourites.application.use_cases.shared.dtos import FavouriteItemDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllFavouritesByUserInputDTO:
    actor_id: UUID
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllFavouritesByUserOutputDTO:
    items: list[FavouriteItemDTO] = field(default_factory=list)
