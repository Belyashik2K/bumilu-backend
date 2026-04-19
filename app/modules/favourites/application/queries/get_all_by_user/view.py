from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
from app.modules.favourites.application.queries.shared.models.favourite_record import (
    FavouriteRecordReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedFavouriteRecordsView:
    user_id: UUID
    favourites: list[FavouriteRecordReadModel] = field(default_factory=list)
    pagination: OffsetPagination
