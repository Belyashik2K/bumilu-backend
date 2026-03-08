from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteReviewCommand:
    actor_id: UUID
    review_id: UUID
