from typing import Any
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

    @staticmethod
    def _build_reviews_base_query(*filters: Any) -> tuple:
        count_stmt = select(func.count()).select_from(ReviewModel).where(*filters)

        items_stmt = (
            select(ReviewModel).where(*filters).options(joinedload(ReviewModel.author))
        )

        return count_stmt, items_stmt

    @staticmethod
    def _to_review_info_view(review: ReviewModel) -> ReviewInfoView:
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
            created_at=review.created_at,
        )

    async def _get_reviews_page(
        self,
        count_stmt,
        items_stmt,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ReviewsPage:
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
            return ReviewsPage(items=[], total=total or 0)

        reviews: list[ReviewModel] = [row.ReviewModel for row in rows]
        total = rows[0].total_count or 0

        return ReviewsPage(
            items=[self._to_review_info_view(review) for review in reviews],
            total=total,
        )

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
        return self._to_review_info_view(review)

    async def get_user_review_for_entity(
        self,
        user_id: UUID,
        entity_type: ReviewEntityTypeEnum,
        entity_id: UUID,
    ) -> ReviewInfoView | None:
        stmt = (
            select(ReviewModel)
            .where(
                ReviewModel.author_id == user_id,
                ReviewModel.entity_type == entity_type,
                ReviewModel.entity_id == entity_id,
            )
            .options(joinedload(ReviewModel.author))
        )
        result = await self._session.execute(stmt)
        review = result.scalar_one_or_none()
        if not review:
            return None
        return self._to_review_info_view(review)

    async def get_all_by_user_id(
        self,
        user_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
        entity_type: ReviewEntityTypeEnum | None = None,
    ) -> ReviewsPage:
        filters = [ReviewModel.author_id == user_id]

        if entity_type is not None:
            filters.append(ReviewModel.entity_type == entity_type)

        count_stmt, items_stmt = self._build_reviews_base_query(*filters)
        return await self._get_reviews_page(
            count_stmt=count_stmt,
            items_stmt=items_stmt,
            limit=limit,
            offset=offset,
        )

    async def get_all_by_entity(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: UUID,
        exclude_review_id: UUID | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ReviewsPage:
        count_stmt, items_stmt = self._build_reviews_base_query(
            ReviewModel.entity_type == entity_type,
            ReviewModel.entity_id == entity_id,
            ReviewModel.id != exclude_review_id if exclude_review_id else True,
        )

        return await self._get_reviews_page(
            count_stmt=count_stmt,
            items_stmt=items_stmt,
            limit=limit,
            offset=offset,
        )
