from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.reviews.application.shared.dtos import ReviewInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllReviewsByUserQuery:
    actor_id: UUID
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllReviewsByUserQueryResult:
    user_id: UUID
    items: list[ReviewInfoDTO] = field(default_factory=list)
