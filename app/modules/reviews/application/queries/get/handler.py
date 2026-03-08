from app.core.application.queries import IQueryHandler
from app.core.shared.domain.value_objects.id import ReviewIdVO
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.queries.get.query import (
    GetReviewQuery,
    GetReviewQueryResult,
)
from app.modules.reviews.application.shared.exceptions import ReviewNotFound


class GetReviewQueryHandler(
    IQueryHandler[
        GetReviewQuery,
        GetReviewQueryResult,
    ]
):
    def __init__(
        self,
        review_repository: IReviewRepository,
    ) -> None:
        self._review_repository = review_repository

    async def handle(
        self,
        query: GetReviewQuery,
    ) -> GetReviewQueryResult:
        review_id = ReviewIdVO.from_uuid(query.review_id)

        review = await self._review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFound(review_id=review_id)

        return GetReviewQueryResult(
            review_id=review.id.value,
            author_id=review.author_id.value,
            entity_type=review.entity_type,
            entity_id=review.entity_id.value,
            rating=review.rating.value,
            text=review.text.value,
        )
