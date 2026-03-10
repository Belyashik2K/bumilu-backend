from app.core.application.queries import IQueryHandler
from app.modules.reviews.application.queries.get.query import (
    GetReviewQuery,
)
from app.modules.reviews.application.queries.readers.review import IReviewReader
from app.modules.reviews.application.queries.shared_views import ReviewInfoView
from app.modules.reviews.application.shared.exceptions import ReviewNotFound


class GetReviewQueryHandler(
    IQueryHandler[
        GetReviewQuery,
        ReviewInfoView,
    ]
):
    def __init__(self, review_reader: IReviewReader) -> None:
        self._review_reader = review_reader

    async def handle(
        self,
        query: GetReviewQuery,
    ) -> ReviewInfoView:
        review = await self._review_reader.get_by_id(query.review_id)
        if not review:
            raise ReviewNotFound(review_id=query.review_id)  # type: ignore

        return review
