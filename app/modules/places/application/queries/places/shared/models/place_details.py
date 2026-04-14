from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
    PlaceCategoryReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_address import (
    BasePlaceAddressReadModel,
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    PlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_photo import (
    PlacePhotoReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_user_context import (
    PlaceUserContextReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)
from app.modules.places.shared.enums.place_status import PlaceStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class BasePlaceDetailsReadModel:
    id: UUID
    timezone: str
    category: PlaceCategoryReadModel
    address: BasePlaceAddressReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceDetailsReadModel(BasePlaceDetailsReadModel):
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoReadModel]
    address: PlaceAddressReadModel
    phones: list[PlacePhoneReadModel] = field(default_factory=list)
    working_days: list[PlaceWorkingDayReadModel] = field(default_factory=list)
    user_context: PlaceUserContextReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPlaceDetailsReadModel(BasePlaceDetailsReadModel):
    status: PlaceStatusEnum
    created_at: datetime
    updated_at: datetime
