from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.constants import UnsetType
from app.core.shared.domain.value_objects.id import (
    ReviewIdVO,
    UserIdVO,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.use_cases.shared.exceptions import (
    ReviewNotFound,
    ReviewOwnershipViolation,
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
        input_data: UpdateReviewInputDTO,
    ) -> UpdateReviewOutputDTO:
        review_id = ReviewIdVO.from_uuid(input_data.review_id)
        review = await self._review_repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFound(review_id=review_id)

        actor_id = UserIdVO.from_uuid(input_data.actor_id)
        if review.author_id != actor_id:
            raise ReviewOwnershipViolation()

        new_rating = (
            ReviewRatingVO(input_data.rating)
            if not isinstance(input_data.rating, UnsetType)
            else review.rating
        )
        new_text = (
            ReviewTextVO(input_data.text)
            if not isinstance(input_data.text, UnsetType)
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
