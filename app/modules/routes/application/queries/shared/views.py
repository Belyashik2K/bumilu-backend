from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.application.queries.places.shared.views import PlaceCardView

# @dataclass(frozen=True, slots=True, kw_only=True)
# class PaginatedRouteCardView:
#     routes: list[RouteCardReadModel] = field(default_factory=list)
#     pagination: OffsetPagination


@dataclass(frozen=True, slots=True, kw_only=True)
class RoutePointView:
    index: int
    preview: PlaceCardView


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteView:
    id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    points: list[RoutePointView] = field(default_factory=list)
    total_points: int
