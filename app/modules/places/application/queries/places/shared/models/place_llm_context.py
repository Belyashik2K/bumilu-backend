from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.queries.places.shared.models.place_address import (
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class NearbyPlaceLLMContextReadModel:
    id: UUID
    title: str
    short_description: str
    category_title: str
    address: PlaceAddressReadModel
    rating: PlaceRatingReadModel
    distance_meters: int | None = field(default=None)
    is_open_now: bool | None = field(default=None)

    def to_llm_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.short_description,
            "category": self.category_title,
            "address": self.address.display,
            "rating": self.rating.average,
            "reviews_count": self.rating.reviews_count,
            "distance_meters": self.distance_meters,
            "is_open_now": self.is_open_now,
        }
