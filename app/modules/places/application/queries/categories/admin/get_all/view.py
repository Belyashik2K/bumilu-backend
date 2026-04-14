from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.categories.shared.models.place_category import (
    AdminPlaceCategoryReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedAdminPlaceCategoriesView:
    categories: list[AdminPlaceCategoryReadModel] = field(default_factory=list)
    pagination: OffsetPagination
