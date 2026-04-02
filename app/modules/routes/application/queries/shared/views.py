from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.places.shared.models.place_card import (
    PlaceCardReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteCardView:
    id: UUID
    title: str
    short_description: str | None = field(default=None)
    total_places: int
    m_to_start_place: int | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteCardPage:
    items: list[RouteCardView]
    total: int


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedRouteCardView:
    routes: list[RouteCardView] = field(default_factory=list)
    pagination: OffsetPagination


@dataclass(frozen=True, slots=True, kw_only=True)
class RoutePointView:
    index: int
    preview: PlaceCardReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteView:
    id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    points: list[RoutePointView] = field(default_factory=list)
    total_points: int
