from dataclasses import dataclass
from uuid import UUID

from app.modules.reviews.application.shared.dtos import ReviewInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetReviewQuery:
    review_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetReviewQueryResult(ReviewInfoDTO): ...
