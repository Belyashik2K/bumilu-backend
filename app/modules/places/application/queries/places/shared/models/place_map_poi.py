from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
    PlaceCategoryReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class BasePlaceMapPOIReadModel:
    id: UUID
    title: str | None = field(default=None)
    location: PlaceLocationReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceMapPOIReadModel(BasePlaceMapPOIReadModel):
    title: str
    category: LocalizedPlaceCategoryReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPlaceMapPOIReadModel(BasePlaceMapPOIReadModel):
    category: PlaceCategoryReadModel
