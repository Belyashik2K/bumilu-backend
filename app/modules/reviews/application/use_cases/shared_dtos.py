from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID


@dataclass(slots=True, kw_only=True, frozen=True)
class ReviewInfoDTO:
    review_id: UUID
    author_id: UUID
    text: str | None = field(default=None)
    rating: int
