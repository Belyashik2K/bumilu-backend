from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.pagination import OffsetPagination
from app.modules.reviews.application.queries.shared.views import (
    ReviewEntityInfoView,
    ReviewInfoView,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedReviewsForEntityView:
    entity: ReviewEntityInfoView
    actor_review: ReviewInfoView | None = field(default=None)
    reviews: list[ReviewInfoView] = field(default_factory=list)
    pagination: OffsetPagination
