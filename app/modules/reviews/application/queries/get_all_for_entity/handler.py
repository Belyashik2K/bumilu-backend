from app.core.application.queries import IQueryHandler
from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.modules.reviews.application.interfaces.entity_resolver import (
    IReviewEntityResolver,
)
from app.modules.reviews.application.interfaces.repositories.review import (
    IReviewRepository,
)
from app.modules.reviews.application.queries.get_all_for_entity.query import (
    GetAllReviewsForEntityQuery,
    GetAllReviewsForEntityQueryResult,
)
from app.modules.reviews.application.shared.dtos import ReviewInfoDTO
from app.modules.reviews.application.shared.exceptions import (
    ReviewEntityNotFound,
)


class GetAllReviewsForEntityQueryHandler(
    IQueryHandler[
        GetAllReviewsForEntityQuery,
        GetAllReviewsForEntityQueryResult,
    ]
):
    def __init__(
        self,
        review_repository: IReviewRepository,
        entity_resolver: IReviewEntityResolver,
    ) -> None:
        self._review_repository = review_repository
        self._entity_resolver = entity_resolver

    async def handle(
        self,
        query: GetAllReviewsForEntityQuery,
    ) -> GetAllReviewsForEntityQueryResult:
        actor_id = UserIdVO.from_uuid(query.actor_id) if query.actor_id else None
        entity_id = IdVO.from_uuid(query.entity_id)

        actor_review = None
        if actor_id:
            actor_review = await self._review_repository.get_by_entity_and_author(
                entity_type=query.entity_type,
                entity_id=entity_id,
                author_id=actor_id,
            )

        reviews = await self._review_repository.get_all_by_entity_excluding_author(
            entity_type=query.entity_type,
            entity_id=entity_id,
            author_id=actor_id,
        )

        if not reviews:
            # If there are no reviews, check if the entity exists
            exists = await self._entity_resolver.resolve(
                entity_type=query.entity_type,
                entity_id=entity_id,
            )
            if not exists:
                raise ReviewEntityNotFound(
                    entity_type=query.entity_type, entity_id=entity_id
                )

        return GetAllReviewsForEntityQueryResult(
            entity_id=query.entity_id,
            entity_type=query.entity_type,
            actor_review=ReviewInfoDTO(
                review_id=actor_review.id.value,
                entity_id=actor_review.entity_id.value,
                entity_type=actor_review.entity_type,
                author_id=actor_review.author_id.value,
                text=actor_review.text.value,
                rating=actor_review.rating.value,
            )
            if actor_review
            else None,
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
