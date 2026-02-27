from dataclasses import dataclass
from uuid import UUID

from app.modules.reviews.application.use_cases.shared.dtos import ReviewInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetReviewInputDTO:
    review_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetReviewOutputDTO(ReviewInfoDTO): ...
