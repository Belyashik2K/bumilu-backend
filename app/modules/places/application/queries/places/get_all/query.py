from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.language import LanguageMixin
from app.core.application.queries.pagination import OffsetPaginationMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllPlacesQuery(LanguageMixin, OffsetPaginationMixin):
    title_like: str | None = field(default=None)
    category_id: UUID | None = field(default=None)
