from app.core.application.use_cases.base import (
    IBaseUseCase,
)
from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.use_cases.create.dtos import (
    CreateReviewInputDTO,
    CreateReviewOutputDTO,
)
from app.modules.reviews.domain.models.review import Review
from app.modules.reviews.domain.value_objects import (
    ReviewRatingVO,
    ReviewTextVO,
)


class CreateReviewUseCase(
    IBaseUseCase[
        CreateReviewInputDTO,
        CreateReviewOutputDTO,
    ]
):
    def __init__(
        self,
        review_repository: IReviewRepository,
    ) -> None:
        self._review_repository = review_repository

    async def execute(self, input_data: CreateReviewInputDTO) -> CreateReviewOutputDTO:
        entity_id = IdVO.from_uuid(input_data.entity_id)
        author_id = UserIdVO.from_uuid(input_data.author_id)

        current_review = await self._review_repository.get_by_entity_and_author(
            entity_type=input_data.entity_type,
            entity_id=entity_id,
            author_id=author_id,
        )
        if current_review is not None:
            raise Exception("You already have a review for this entity")

        review = Review.create(
            author_id=author_id,
            entity_type=input_data.entity_type,
            entity_id=entity_id,
            text=ReviewTextVO(input_data.text),
            rating=ReviewRatingVO(input_data.rating),
        )
        await self._review_repository.save(review)

        return CreateReviewOutputDTO(
            id=review.id.value,
        )
