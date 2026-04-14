from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.modules.places.application.queries.places.shared.models.place_translation import (
    PlaceTranslationReadModel,
)


class IPlaceTranslationReader(ABC):
    @abstractmethod
    async def list_by_place_id(
        self,
        place_id: UUID,
        limit: int,
        offset: int,
    ) -> PageReadModel[PlaceTranslationReadModel]: ...
