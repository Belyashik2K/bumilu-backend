from app.core.application.queries import IQueryHandler
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.queries.get_all_by_user import (
    GetAllReviewsByUserQuery,
    GetAllReviewsByUserQueryResult,
)
from app.modules.reviews.application.shared.dtos import ReviewInfoDTO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.get.exceptions import UserNotFound


class GetAllReviewsByUserQueryHandler(
    IQueryHandler[GetAllReviewsByUserQuery, GetAllReviewsByUserQueryResult]
):
    def __init__(
        self, review_repository: IReviewRepository, user_repository: IUserRepository
    ) -> None:
        self._review_repository = review_repository
        self._user_repository = user_repository

    async def handle(
        self,
        query: GetAllReviewsByUserQuery,
    ) -> GetAllReviewsByUserQueryResult:
        author_id = UserIdVO.from_uuid(query.user_id)

        if not await self._user_repository.get_by_id(
            author_id
        ):  # TODO: minimize contacts with other domains
            raise UserNotFound(author_id)

        reviews = await self._review_repository.get_all_by_author(
            author_id=author_id,
        )

        return GetAllReviewsByUserQueryResult(
            user_id=author_id.value,
            items=[
                ReviewInfoDTO(
                    review_id=review.id.value,
                    author_id=review.author_id.value,
                    entity_type=review.entity_type,
                    entity_id=review.entity_id.value,
                    text=review.text.value,
                    rating=review.rating.value,
                )
                for review in reviews
            ],
        )
