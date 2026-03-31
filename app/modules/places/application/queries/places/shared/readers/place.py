from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.places.application.queries.places.shared.views import (
    PlaceCardPage,
    PlaceView,
)


class IPlaceReader(ABC):
    @abstractmethod
    async def get_by_id(
        self, place_id: UUID, translation_language: LanguageEnum
    ) -> PlaceView | None: ...

    @abstractmethod
    async def list(
        self,
        *,
        title_like: str | None,
        category_id: UUID | None,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PlaceCardPage: ...
