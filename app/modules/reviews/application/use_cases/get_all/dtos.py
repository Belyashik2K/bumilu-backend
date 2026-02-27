from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.reviews.application.use_cases.shared.shared_dtos import ReviewInfoDTO
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllReviewsForEntityInputDTO:
    entity_id: UUID
    entity_type: ReviewEntityTypeEnum
    filters: None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllReviewsForEntityOutputDTO:
    entity_id: UUID
    items: list[ReviewInfoDTO] = field(default_factory=list)
