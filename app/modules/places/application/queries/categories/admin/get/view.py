from dataclasses import dataclass

from app.modules.places.application.queries.categories.shared.models.place_category import (
    PlaceCategoryReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPlaceCategoryView(PlaceCategoryReadModel): ...
