from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
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
from app.modules.places.application.queries.places.shared.models.place_working_hour import (
    PlaceWorkingHourReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardReadModel:
    id: UUID
    title: str
    short_description: str | None = field(default=None)
    timezone: str
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoReadModel] = field(default_factory=list)
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    working_hours: list[PlaceWorkingHourReadModel] = field(default_factory=list)
