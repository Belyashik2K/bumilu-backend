from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.places.application.queries.places.shared.views import PlaceView


class IPlaceReader(ABC):
    @abstractmethod
    async def get_by_id(
        self, place_id: UUID, translation_language: LanguageEnum
    ) -> PlaceView | None: ...
