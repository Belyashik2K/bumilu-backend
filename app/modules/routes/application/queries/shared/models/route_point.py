from dataclasses import dataclass

from app.modules.places.application.queries.places.shared.models.place_card import (
    PlaceCardReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteWaypointModel:
    index: int
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True, kw_only=True)
class RoutePointReadModel:
    index: int
    preview: PlaceCardReadModel
