import logging

from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import (
    ReviewIdVO,
    UserIdVO,
)
from app.core.shared.utils import prepare_extras
from app.modules.reviews.application.commands.delete import (
    DeleteReviewInputDTO,
    DeleteReviewOutputDTO,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.shared.exceptions import (
    ReviewNotFound,
    ReviewOwnershipViolation,
)

logger = logging.getLogger(__name__)


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

        review = await self._review_repository.get_by_id(
            review_id
        )  # TODO: idempotent delete
        if not review:
            raise ReviewNotFound(review_id=review_id)

        actor_id = UserIdVO.from_uuid(input_data.actor_id)
        if review.author_id != actor_id:
            logger.warning(
                "review_delete_forbidden",
                extra=prepare_extras(
                    review_id=str(review.id),
                    actor_user_id=str(actor_id),
                    owner_user_id=str(review.author_id),
                ),
            )
            raise ReviewOwnershipViolation()

        await self._review_repository.delete_by_id(review_id)

        return DeleteReviewOutputDTO()
