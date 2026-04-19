from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.core.application.queries.pagination import OffsetPaginationMixin
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllReviewsForEntityQuery(OffsetPaginationMixin):
    actor_id: UUID
    entity_id: UUID
    entity_type: ReviewEntityTypeEnum
