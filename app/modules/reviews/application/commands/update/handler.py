import logging

from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.constants import UnsetType
from app.core.shared.domain.value_objects.id import (
    PrincipalIdVO,
    ReviewIdVO,
)
from app.core.shared.utils import prepare_extras
from app.modules.reviews.application.commands.update import (
    UpdateReviewCommand,
    UpdateReviewCommandResult,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.shared.exceptions import (
    ReviewNotFound,
    ReviewOwnershipViolation,
)
from app.modules.reviews.domain.value_objects import (
    ReviewRatingVO,
    ReviewTextVO,
)

logger = logging.getLogger(__name__)


class UpdateReviewCommandHandler(
    ICommandHandlerWithResult[UpdateReviewCommand, UpdateReviewCommandResult]
):
    def __init__(
        self,
        review_repository: IReviewRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._review_repository = review_repository

    async def handle(
        self,
        command: UpdateReviewCommand,
    ) -> UpdateReviewCommandResult:
        review_id = ReviewIdVO.from_uuid(command.review_id)
        review = await self._review_repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFound(review_id=review_id)

        actor_id = PrincipalIdVO.from_uuid(command.actor_id)
        if review.author_id != actor_id:
            logger.warning(
                "review_update_forbidden",
                extra=prepare_extras(
                    review_id=str(review.id),
                    actor_user_id=str(actor_id),
                    owner_user_id=str(review.author_id),
                ),
            )
            raise ReviewOwnershipViolation()

        new_rating = (
            ReviewRatingVO(command.rating)
            if not isinstance(command.rating, UnsetType)
            else review.rating
        )
        new_text = (
            ReviewTextVO(command.text)
            if not isinstance(command.text, UnsetType)
            else review.text
        )

        review.update(
            rating=new_rating,
            text=new_text,
        )
        await self._review_repository.save(review)

        return UpdateReviewCommandResult(
            review_id=review.id.value,
            rating=review.rating.value,
            text=review.text.value,
        )
