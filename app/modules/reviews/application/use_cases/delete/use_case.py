from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import (
    ReviewIdVO,
    UserIdVO,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.use_cases.delete import (
    DeleteReviewInputDTO,
    DeleteReviewOutputDTO,
)


class DeleteReviewUseCase(
    IBaseUseCase[
        DeleteReviewInputDTO,
        DeleteReviewOutputDTO,
    ]
):
    def __init__(self, review_repository: IReviewRepository) -> None:
        self._review_repository = review_repository

    async def execute(self, input_data: DeleteReviewInputDTO) -> DeleteReviewOutputDTO:
        review_id = ReviewIdVO.from_uuid(input_data.review_id)

        review = await self._review_repository.get_by_id(review_id)
        if not review:
            raise Exception("Review not found")

        actor_id = UserIdVO.from_uuid(input_data.actor_id)
        if review.author_id != actor_id:
            raise Exception("Unauthorized")  # TODO: Custom exception

        await self._review_repository.delete(review)

        return DeleteReviewOutputDTO()
