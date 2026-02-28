from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.use_cases.get_all_by_user import (
    GetAllReviewsByUserInputDTO,
    GetAllReviewsByUserOutputDTO,
)
from app.modules.reviews.application.use_cases.shared.dtos import ReviewInfoDTO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.use_cases.get.exceptions import UserNotFound


class GetAllReviewsByUserUseCase(
    IBaseUseCase[GetAllReviewsByUserInputDTO, GetAllReviewsByUserOutputDTO]
):
    def __init__(
        self, review_repository: IReviewRepository, user_repository: IUserRepository
    ) -> None:
        self._review_repository = review_repository
        self._user_repository = user_repository

    async def execute(
        self,
        input_data: GetAllReviewsByUserInputDTO,
    ) -> GetAllReviewsByUserOutputDTO:
        author_id = UserIdVO.from_uuid(input_data.user_id)

        if not await self._user_repository.get_by_id(
            author_id
        ):  # TODO: minimize contacts with other domains
            raise UserNotFound(author_id)

        reviews = await self._review_repository.get_all_by_author(
            author_id=author_id,
        )

        return GetAllReviewsByUserOutputDTO(
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
