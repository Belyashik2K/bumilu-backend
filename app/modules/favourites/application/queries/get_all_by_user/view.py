from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.shared.application.queries.pagination import OffsetPagination
from app.modules.favourites.application.queries.shared_views import FavouriteEntityView


@dataclass(frozen=True, slots=True, kw_only=True)
class FavouritesPage:
    items: list[FavouriteEntityView]
    total: int


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedFavouritesView:
    user_id: UUID
    favourites: list[FavouriteEntityView] = field(default_factory=list)
    pagination: OffsetPagination
