from dataclasses import dataclass

from app.modules.places.application.queries.places.shared.models.place_card import (
    AdminPlaceCardReadModel,
    PlaceCardReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseRoutePointModel:
    index: int


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteWaypointModel(BaseRoutePointModel):
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True, kw_only=True)
class RoutePointReadModel(BaseRoutePointModel):
    preview: PlaceCardReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminRoutePointReadModel(BaseRoutePointModel):
    preview: AdminPlaceCardReadModel
