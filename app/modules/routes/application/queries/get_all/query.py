from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.language import LanguageMixin
from app.core.application.queries.pagination import OffsetPaginationMixin
from app.modules.places.shared.enums.route_sort import RouteSortByEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllRoutesQuery(LanguageMixin, OffsetPaginationMixin):
    latitude: float | None = field(default=None)
    longitude: float | None = field(default=None)
    sort_by: RouteSortByEnum | None = field(default=None)
