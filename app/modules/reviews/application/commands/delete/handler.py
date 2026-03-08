import logging

from app.core.application.commands import ICommandHandler
from app.core.shared.domain.value_objects.id import (
    ReviewIdVO,
    UserIdVO,
)
from app.core.shared.utils import prepare_extras
from app.modules.reviews.application.commands.delete import (
    DeleteReviewCommand,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.shared.exceptions import (
    ReviewOwnershipViolation,
)

logger = logging.getLogger(__name__)


class DeleteReviewCommandHandler(ICommandHandler[DeleteReviewCommand]):
    def __init__(self, review_repository: IReviewRepository) -> None:
        self._review_repository = review_repository

    async def handle(self, command: DeleteReviewCommand) -> None:
        review_id = ReviewIdVO.from_uuid(command.review_id)

        review = await self._review_repository.get_by_id(review_id)
        if not review:
            return None

        actor_id = UserIdVO.from_uuid(command.actor_id)
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

        return None
