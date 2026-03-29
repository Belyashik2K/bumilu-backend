from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
from app.modules.reviews.application.queries.shared.views import ReviewInfoView


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedReviewsByUserView:
    user_id: UUID
    reviews: list[ReviewInfoView] = field(default_factory=list)
    pagination: OffsetPagination
