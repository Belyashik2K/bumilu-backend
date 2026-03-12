from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.modules.reviews.application.queries.shared_views import (
    ReviewInfoView,
    ReviewsPage,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class IReviewReader(ABC):
    @abstractmethod
    async def get_by_id(self, review_id: UUID) -> ReviewInfoView | None: ...

    @abstractmethod
    async def get_user_review_for_entity(
        self,
        user_id: UUID,
        entity_type: ReviewEntityTypeEnum,
        entity_id: UUID,
    ) -> ReviewInfoView | None: ...

    @abstractmethod
    async def get_all_by_user_id(
        self,
        user_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
        entity_type: ReviewEntityTypeEnum | None = None,
    ) -> ReviewsPage: ...

    @abstractmethod
    async def get_all_by_entity(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: UUID,
        exclude_author_id: UUID | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ReviewsPage: ...
