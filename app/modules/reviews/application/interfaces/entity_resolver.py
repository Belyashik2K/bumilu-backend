from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.entity_resolver import IEntityResolver
from app.core.shared.domain.value_objects.id import IdVO
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class IReviewEntityResolver(IEntityResolver, ABC):
    @abstractmethod
    async def resolve(
        self,
        entity_type: ReviewEntityTypeEnum,
        entity_id: IdVO,
    ) -> bool: ...
