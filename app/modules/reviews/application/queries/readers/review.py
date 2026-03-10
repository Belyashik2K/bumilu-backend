from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.modules.reviews.application.queries.shared_views import ReviewInfoView


class IReviewReader(ABC):
    @abstractmethod
    async def get_by_id(self, review_id: UUID) -> ReviewInfoView | None: ...
