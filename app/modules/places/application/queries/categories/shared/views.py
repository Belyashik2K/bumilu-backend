from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategoryView:
    id: UUID
    slug: str
    icon_key: str
    marker_color: str
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategoriesPage:  # TODO: Generic class instead of creating a new one for each entity
    items: list[PlaceCategoryView]
    total: int


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedPlaceCategoriesView:
    categories: list[PlaceCategoryView] = field(default_factory=list)
    pagination: OffsetPagination
