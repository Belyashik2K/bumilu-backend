from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_address import (
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


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceDetailsReadModel:
    id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    timezone: str
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoReadModel]
    address: PlaceAddressReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    phones: list[PlacePhoneReadModel] = field(default_factory=list)
    working_days: list[PlaceWorkingDayReadModel] = field(default_factory=list)
    user_context: PlaceUserContextReadModel
