from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.places.shared.dtos import BBox
from app.modules.places.application.queries.places.shared.models.place_card import (
    AdminPlaceCardReadModel,
    PlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    AdminPlaceDetailsReadModel,
    PlaceDetailsReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_map_poi import (
    AdminPlaceMapPOIReadModel,
    PlaceMapPOIReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    AdminPlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_photo import (
    AdminPlacePhotoReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)


class IPlaceReader(ABC):
    @abstractmethod
    async def exists(self, place_id: UUID) -> bool: ...

    @abstractmethod
    async def count_by_category_id(self, category_id: UUID) -> int: ...

    @abstractmethod
    async def get_by_id(
        self,
        *,
        actor_id: UUID | None = None,
        place_id: UUID,
        translation_language: LanguageEnum,
    ) -> PlaceDetailsReadModel | None: ...

    @abstractmethod
    async def get_admin_details_by_id(
        self,
        place_id: UUID,
    ) -> AdminPlaceDetailsReadModel | None: ...

    @abstractmethod
    async def get_cards_by_ids(
        self,
        place_ids: list[UUID],
        translation_language: LanguageEnum,
    ) -> list[PlaceCardReadModel]: ...

    @abstractmethod
    async def get_all(
        self,
        *,
        title_like: str | None,
        category_slug: str | None,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PageReadModel[PlaceCardReadModel]: ...

    @abstractmethod
    async def admin_get_all(
        self,
        *,
        title_like: str | None,
        category_slug: str | None,
        limit: int,
        offset: int,
    ) -> PageReadModel[AdminPlaceCardReadModel]: ...

    @abstractmethod
    async def list_poi_in_bounds(
        self,
        *,
        bounds: BBox,
        translation_language: LanguageEnum,
        limit: int,
    ) -> list[PlaceMapPOIReadModel]: ...

    @abstractmethod
    async def list_admin_poi_in_bounds(
        self,
        *,
        bounds: BBox,
        translation_language: LanguageEnum,
        limit: int,
    ) -> list[AdminPlaceMapPOIReadModel]: ...

    @abstractmethod
    async def get_admin_photos_by_id(
        self,
        place_id: UUID,
    ) -> list[AdminPlacePhotoReadModel]: ...

    @abstractmethod
    async def get_admin_phones_by_id(
        self,
        place_id: UUID,
    ) -> list[AdminPlacePhoneReadModel]: ...

    @abstractmethod
    async def get_working_days_by_id(
        self,
        place_id: UUID,
    ) -> list[PlaceWorkingDayReadModel]: ...

    @abstractmethod
    async def get_working_day_by_weekday(
        self,
        place_id: UUID,
        weekday: int,
    ) -> PlaceWorkingDayReadModel | None: ...
