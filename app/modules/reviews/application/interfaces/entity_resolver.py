from abc import (
    ABC,
    abstractmethod,
)

from app.core.shared.domain.value_objects.id import IdVO
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class IEntityResolver(ABC):
    @abstractmethod
    async def resolve(
        self, entity_type: ReviewEntityTypeEnum, entity_id: IdVO
    ) -> bool: ...
