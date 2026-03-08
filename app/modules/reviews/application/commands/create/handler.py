from app.core.application.commands import ICommandHandlerWithResult
from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.modules.reviews.application.commands.create import (
    CreateReviewCommand,
    CreateReviewCommandResult,
)
from app.modules.reviews.application.commands.create.exceptions import (
    ReviewAlreadyExists,
)
from app.modules.reviews.application.interfaces.entity_resolver import (
    IReviewEntityResolver,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.shared.exceptions import (
    ReviewEntityNotFound,
)
from app.modules.reviews.domain.models.review import Review
from app.modules.reviews.domain.value_objects import (
    ReviewRatingVO,
    ReviewTextVO,
)


class CreateReviewCommandHandler(
    ICommandHandlerWithResult[
        CreateReviewCommand,
        CreateReviewCommandResult,
    ]
):
    def __init__(
        self,
        review_repository: IReviewRepository,
        entity_resolver: IReviewEntityResolver,
    ) -> None:
        self._review_repository = review_repository
        self._entity_resolver = entity_resolver

    async def handle(self, command: CreateReviewCommand) -> CreateReviewCommandResult:
        entity_id = IdVO.from_uuid(command.entity_id)
        author_id = UserIdVO.from_uuid(command.author_id)

        current_review = await self._review_repository.get_by_entity_and_author(
            entity_type=command.entity_type,
            entity_id=entity_id,
            author_id=author_id,
        )
        if current_review is not None:
            raise ReviewAlreadyExists(entity_type=command.entity_type)

        exists = await self._entity_resolver.resolve(
            entity_type=command.entity_type,
            entity_id=entity_id,
        )
        if not exists:
            raise ReviewEntityNotFound(
                entity_type=command.entity_type,
                entity_id=entity_id,
            )

        review = Review.create(
            author_id=author_id,
            entity_type=command.entity_type,
            entity_id=entity_id,
            text=ReviewTextVO(command.text),
            rating=ReviewRatingVO(command.rating),
        )
        await self._review_repository.save(review)

        return CreateReviewCommandResult(
            review_id=review.id.value,
            entity_type=review.entity_type,
            entity_id=review.entity_id.value,
            author_id=review.author_id.value,
            text=review.text.value,
            rating=review.rating.value,
        )
