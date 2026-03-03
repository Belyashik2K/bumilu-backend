from app.core.shared.domain.value_objects.id import IdVO
from app.modules.reviews.application.interfaces.entity_resolver import (
    IReviewEntityResolver,
)
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class ReviewEntityResolver(IReviewEntityResolver):
    async def resolve(self, entity_type: ReviewEntityTypeEnum, entity_id: IdVO) -> bool:
        return True  # TODO: Implement actual logic, when other services are implemented
