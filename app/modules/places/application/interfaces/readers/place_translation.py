from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.places.shared.models.place_translation import (
    PlaceTranslationReadModel,
)


class IPlaceTranslationReader(ABC):
    @abstractmethod
    async def get_by_place_id_and_language_code(
        self,
        place_id: UUID,
        language_code: LanguageEnum,
    ) -> PlaceTranslationReadModel | None: ...

    @abstractmethod
    async def list_by_place_id(
        self,
        place_id: UUID,
        limit: int,
        offset: int,
    ) -> PageReadModel[PlaceTranslationReadModel]: ...
