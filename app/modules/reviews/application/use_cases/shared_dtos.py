from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(slots=True, kw_only=True, frozen=True)
class ReviewInfoDTO:
    review_id: UUID
    entity_id: UUID
    entity_type: ReviewEntityTypeEnum
    author_id: UUID
    text: str | None = field(default=None)
    rating: int
