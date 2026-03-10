from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateReviewCommand:
    entity_id: UUID
    entity_type: ReviewEntityTypeEnum
    author_id: UUID
    text: str | None = field(default=None)
    rating: int


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateReviewCommandResult:
    review_id: UUID
