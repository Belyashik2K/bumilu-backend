from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import IdVO
from app.modules.reviews.application.interfaces.entity_resolver import IEntityResolver
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.use_cases.get_all import (
    GetAllReviewsForEntityInputDTO,
    GetAllReviewsForEntityOutputDTO,
)
from app.modules.reviews.application.use_cases.shared_dtos import ReviewInfoDTO


class GetAllReviewsForEntityUseCase(
    IBaseUseCase[
        GetAllReviewsForEntityInputDTO,
        GetAllReviewsForEntityOutputDTO,
    ]
):
    def __init__(
        self, review_repository: IReviewRepository, entity_resolver: IEntityResolver
    ) -> None:
        self._review_repository = review_repository
        self._entity_resolver = entity_resolver

    async def execute(
        self,
        input_data: GetAllReviewsForEntityInputDTO,
    ) -> GetAllReviewsForEntityOutputDTO:
        entity_id = IdVO.from_uuid(input_data.entity_id)

        reviews = await self._review_repository.get_all_by_entity(
            entity_type=input_data.entity_type,
            entity_id=entity_id,
        )

        if not reviews:
            # If there are no reviews, check if the entity exists
            exists = await self._entity_resolver.resolve(
                entity_type=input_data.entity_type,
                entity_id=entity_id,
            )
            if not exists:
                raise Exception("Entity not found")

        return GetAllReviewsForEntityOutputDTO(
            entity_id=entity_id.value,
            items=[
                ReviewInfoDTO(
                    review_id=review.id.value,
                    entity_id=review.entity_id.value,
                    entity_type=review.entity_type,
                    author_id=review.author_id.value,
                    text=review.text.value,
                    rating=review.rating.value,
                )
                for review in reviews
            ],
        )
