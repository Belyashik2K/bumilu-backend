from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.reviews.application.queries.get_all_by_user.query import (
    GetAllReviewsByUserQuery,
)
from app.modules.reviews.application.queries.get_all_by_user.view import (
    PaginatedReviewsByUserView,
)
from app.modules.reviews.application.queries.readers.review import IReviewReader
from app.modules.users.application.queries.get.exceptions import UserNotFound
from app.modules.users.application.queries.readers.user import IUserReader


class GetAllReviewsByUserQueryHandler(
    IQueryHandler[GetAllReviewsByUserQuery, PaginatedReviewsByUserView]
):
    def __init__(
        self,
        review_reader: IReviewReader,
        user_reader: IUserReader,
    ) -> None:
        self._review_reader = review_reader
        self._user_reader = user_reader

    async def handle(
        self,
        query: GetAllReviewsByUserQuery,
    ) -> PaginatedReviewsByUserView:
        author_id = query.user_id

        if not await self._user_reader.get_by_id(
            author_id
        ):  # TODO: minimize contacts with other domains
            raise UserNotFound(author_id)  # type: ignore

        data = await self._review_reader.get_all_by_user_id(
            user_id=author_id,
            limit=query.limit,
            offset=query.offset,
            entity_type=query.entity_type,
        )

        return PaginatedReviewsByUserView(
            user_id=author_id,
            reviews=data.items,
            pagination=OffsetPagination.create(
                limit=query.limit,
                offset=query.offset,
                total=data.total,
            ),
        )
