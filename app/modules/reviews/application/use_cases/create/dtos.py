from dataclasses import dataclass
from uuid import UUID

from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateReviewInputDTO:
    entity_id: UUID
    entity_type: ReviewEntityTypeEnum
    author_id: UUID
    text: str
    rating: int


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateReviewOutputDTO:
    id: UUID
