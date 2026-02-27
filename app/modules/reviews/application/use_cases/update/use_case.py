from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.constants import UnsetType
from app.core.shared.domain.value_objects.id import (
    ReviewIdVO,
    UserIdVO,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.use_cases.update import (
    UpdateReviewInputDTO,
    UpdateReviewOutputDTO,
)
from app.modules.reviews.domain.value_objects import (
    ReviewRatingVO,
    ReviewTextVO,
)


class UpdateReviewUseCase(IBaseUseCase[UpdateReviewInputDTO, UpdateReviewOutputDTO]):
    def __init__(
        self,
        review_repository: IReviewRepository,
    ) -> None:
        self._review_repository = review_repository

    async def execute(
        self,
        input_dto: UpdateReviewInputDTO,
    ) -> UpdateReviewOutputDTO:
        review_id = ReviewIdVO.from_uuid(input_dto.review_id)
        review = await self._review_repository.get_by_id(review_id)
        if review is None:
            raise Exception("Review not found")  # TODO: Custom exception

        actor_id = UserIdVO.from_uuid(input_dto.actor_id)
        if review.author_id != actor_id:
            raise Exception("Unauthorized")  # TODO: Custom exception

        new_rating = (
            ReviewRatingVO(input_dto.rating)
            if not isinstance(input_dto.rating, UnsetType)
            else review.rating
        )
        new_text = (
            ReviewTextVO(input_dto.text)
            if not isinstance(input_dto.text, UnsetType)
            else review.text
        )

        review.update(
            rating=new_rating,
            text=new_text,
        )
        await self._review_repository.save(review)

        return UpdateReviewOutputDTO(
            review_id=review.id.value,
            rating=review.rating.value,
            text=review.text.value,
        )
