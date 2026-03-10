from app.core.application.queries import IQueryHandler
from app.core.shared.application.queries.pagination import OffsetPagination
from app.core.shared.domain.value_objects.id import (
    IdVO,
)
from app.modules.reviews.application.interfaces.entity_resolver import (
    IReviewEntityResolver,
)
from app.modules.reviews.application.queries.get_all_for_entity.query import (
    GetAllReviewsForEntityQuery,
)
from app.modules.reviews.application.queries.get_all_for_entity.view import (
    PaginatedReviewsForEntityView,
)
from app.modules.reviews.application.queries.readers.review import IReviewReader
from app.modules.reviews.application.queries.shared_views import (
    ReviewEntityInfoView,
)
from app.modules.reviews.application.shared.exceptions import (
    ReviewEntityNotFound,
)


class GetAllReviewsForEntityQueryHandler(
    IQueryHandler[
        GetAllReviewsForEntityQuery,
        PaginatedReviewsForEntityView,
    ]
):
    def __init__(
        self,
        review_reader: IReviewReader,
        entity_resolver: IReviewEntityResolver,
    ) -> None:
        self._review_reader = review_reader
        self._entity_resolver = entity_resolver

    async def handle(
        self,
        query: GetAllReviewsForEntityQuery,
    ) -> PaginatedReviewsForEntityView:
        actor_id = query.actor_id
        entity_id = query.entity_id

        actor_review = await self._review_reader.get_user_review_for_entity(
            user_id=actor_id,
            entity_type=query.entity_type,
            entity_id=entity_id,
        )

        reviews = await self._review_reader.get_all_by_entity(
            entity_type=query.entity_type,
            entity_id=entity_id,
            exclude_review_id=actor_review.review_id if actor_review else None,
            limit=query.limit,
            offset=query.offset,
        )

        if not reviews:
            # If there are no reviews, check if the entity exists
            entity_id_vo = IdVO.from_uuid(query.entity_id)
            exists = await self._entity_resolver.resolve(
                entity_type=query.entity_type,
                entity_id=entity_id_vo,
            )
            if not exists:
                raise ReviewEntityNotFound(
                    entity_type=query.entity_type, entity_id=entity_id_vo
                )

        return PaginatedReviewsForEntityView(
            entity=ReviewEntityInfoView(
                id=entity_id,
                type=query.entity_type,
            ),
            actor_review=actor_review,
            reviews=reviews.items,
            pagination=OffsetPagination.create(
                limit=query.limit,
                offset=query.offset,
                total=reviews.total,
            ),
        )
