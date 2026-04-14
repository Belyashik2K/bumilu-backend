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
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_photo import (
    PlacePhotoReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class BasePlaceCardReadModel:
    id: UUID
    timezone: str
    category: PlaceCategoryReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardReadModel(BasePlaceCardReadModel):
    title: str
    short_description: str | None = field(default=None)
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoReadModel] = field(default_factory=list)
    working_days: list[PlaceWorkingDayReadModel] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPlaceCardReadModel(
    PlaceCardReadModel
):  # TODO: add title and short description translations when language support will be implemented
    created_at: datetime
    updated_at: datetime
