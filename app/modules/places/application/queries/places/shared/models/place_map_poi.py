from dataclasses import dataclass
from uuid import UUID

from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceMapPOIReadModel:
    id: UUID
    title: str
    category: LocalizedPlaceCategoryReadModel
    location: PlaceLocationReadModel
