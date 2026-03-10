from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.modules.reviews.application.queries.readers.review import IReviewReader
from app.modules.reviews.application.queries.shared_views import (
    ReviewAuthorInfoView,
    ReviewEntityInfoView,
    ReviewInfoView,
)
from app.modules.reviews.infrastructure.database.models import ReviewModel


class SQLAlchemyReviewReader(IReviewReader):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_by_id(self, review_id: UUID) -> ReviewInfoView | None:
        stmt = (
            select(ReviewModel)
            .where(ReviewModel.id == review_id)
            .options(joinedload(ReviewModel.author))
        )
        result = await self._session.execute(stmt)
        review = result.scalar_one_or_none()
        if not review:
            return None
        return ReviewInfoView(
            review_id=review.id,
            entity=ReviewEntityInfoView(
                id=review.entity_id,
                type=review.entity_type,
            ),
            author=ReviewAuthorInfoView(
                id=review.author_id,
            ),
            text=review.text,
            rating=review.rating,
        )
