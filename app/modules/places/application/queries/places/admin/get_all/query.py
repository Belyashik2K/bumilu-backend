from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.pagination import (
    OffsetPaginationMixin,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminPlacesListQuery(OffsetPaginationMixin):
    title_like: str | None = field(default=None)
    category_slug: str | None = field(default=None)
