from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.shared.constants import (
    UNSET,
    UnsetType,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateReviewInputDTO:
    actor_id: UUID
    review_id: UUID
    text: str | None | UnsetType = field(default=UNSET)
    rating: int | UnsetType = field(default=UNSET)


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateReviewOutputDTO:
    review_id: UUID
    text: str | None = field(default=None)
    rating: int
