from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.modules.reviews.application.queries.readers.review import IReviewReader
from app.modules.reviews.application.queries.shared_views import (
    ReviewAuthorInfoView,
    ReviewEntityInfoView,
    ReviewInfoView,
    ReviewsPage,
)
from app.modules.reviews.infrastructure.database.models import ReviewModel
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


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

    async def get_all_by_user_id(
        self,
        user_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
        entity_type: ReviewEntityTypeEnum | None = None,
    ) -> ReviewsPage:
        count_stmt = (
            select(func.count())
            .select_from(ReviewModel)
            .where(ReviewModel.author_id == user_id)
        )
        items_stmt = (
            select(ReviewModel)
            .where(ReviewModel.author_id == user_id)
            .options(joinedload(ReviewModel.author))
        )

        if entity_type is not None:
            count_stmt = count_stmt.where(ReviewModel.entity_type == entity_type)
            items_stmt = items_stmt.where(ReviewModel.entity_type == entity_type)

        total_subquery = count_stmt.scalar_subquery()
        stmt = (
            items_stmt.add_columns(total_subquery.label("total_count"))
            .order_by(ReviewModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            total = await self._session.scalar(count_stmt)
            return ReviewsPage(
                items=[],
                total=total or 0,
            )

        reviews: list[ReviewModel] = [row.ReviewModel for row in rows]
        total = rows[0].total_count

        return ReviewsPage(
            items=[
                ReviewInfoView(
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
                for review in reviews
            ],
            total=total or 0,
        )
