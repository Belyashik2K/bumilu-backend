from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.shared.domain.value_objects.id import (
    IdVO,
    ReviewIdVO,
    UserIdVO,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.domain.models.review import Review
from app.modules.reviews.domain.value_objects import (
    ReviewRatingVO,
    ReviewTextVO,
)
from app.modules.reviews.infrastructure.database.models import ReviewModel
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class SQLAlchemyReviewRepository(
    IReviewRepository,
    SQLAlchemyBaseRepository[Review, ReviewModel],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ReviewModel)

    def _to_entity(self, review: ReviewModel) -> Review:
        return Review(
            id=ReviewIdVO.from_uuid(review.id),
            author_id=UserIdVO.from_uuid(review.author_id),
            entity_type=review.entity_type,
            entity_id=IdVO.from_uuid(review.entity_id),
            text=ReviewTextVO(review.text),
            rating=ReviewRatingVO(review.rating),
        )

    def _to_data(self, review: Review) -> ReviewModel:
        return ReviewModel(
            id=review.id.value,
            author_id=review.author_id.value,
            entity_type=review.entity_type,
            entity_id=review.entity_id.value,
            text=review.text.value,
            rating=review.rating.value,
        )

    async def get_by_entity_and_author(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
        author_id: UserIdVO,
    ) -> Review | None:
        stmt = select(ReviewModel).where(
            ReviewModel.entity_type == entity_type,
            ReviewModel.entity_id == entity_id.value,
            ReviewModel.author_id == author_id.value,
        )
        result = await self.session.execute(stmt)
        review_model = result.scalar_one_or_none()
        if review_model is None:
            return None
        return self._to_entity(review_model)

    async def get_all_by_entity(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
    ) -> list[Review]:
        stmt = select(ReviewModel).where(
            ReviewModel.entity_type == entity_type,
            ReviewModel.entity_id == entity_id.value,
        )
        result = await self.session.execute(stmt)
        review_models = result.scalars().all()
        return [self._to_entity(review_model) for review_model in review_models]

    async def delete_by_id(self, review_id: ReviewIdVO) -> None:
        stmt = delete(ReviewModel).where(
            ReviewModel.id == review_id.value,
        )
        await self.session.execute(stmt)
