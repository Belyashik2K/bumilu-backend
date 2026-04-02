from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.queries.places.shared.models.place_address import (
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    PlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_hour import (
    PlaceWorkingHourReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceDetailsReadModel:
    id: UUID
    category_id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    timezone: str
    address: PlaceAddressReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    phones: list[PlacePhoneReadModel]
    working_hours: list[PlaceWorkingHourReadModel]
