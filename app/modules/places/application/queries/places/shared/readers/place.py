from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.places.application.queries.places.get_map_poi.query import BBox
from app.modules.places.application.queries.places.shared.views import (
    PlaceCardPage,
    PlaceMapPOIView,
    PlaceView,
)


class IPlaceReader(ABC):
    @abstractmethod
    async def get_by_id(
        self, place_id: UUID, translation_language: LanguageEnum
    ) -> PlaceView | None: ...

    @abstractmethod
    async def get_all(
        self,
        *,
        title_like: str | None,
        category_id: UUID | None,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PlaceCardPage: ...

    @abstractmethod
    async def list_poi_in_bounds(
        self,
        *,
        bounds: BBox,
        translation_language: LanguageEnum,
        limit: int,
    ) -> list[PlaceMapPOIView]: ...
