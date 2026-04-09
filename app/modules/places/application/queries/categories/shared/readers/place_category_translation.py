from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.modules.places.application.queries.categories.shared.models.place_category import (
    PlaceCategoryTranslationReadModel,
)


class IPlaceCategoryTranslationReader(ABC):
    @abstractmethod
    async def list_by_category_id(
        self,
        category_id: UUID,
    ) -> list[PlaceCategoryTranslationReadModel]: ...
