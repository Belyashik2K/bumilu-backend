from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.pagination import (
    OffsetPaginationMixin,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllReviewsByUserQuery(OffsetPaginationMixin):
    actor_id: UUID
    user_id: UUID
    entity_type: ReviewEntityTypeEnum | None = field(default=None)
