from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.pagination import OffsetPagination


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteCardView:
    id: str
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
