from dataclasses import dataclass

from app.core.application.queries.language import LanguageMixin
from app.core.application.queries.pagination import OffsetPaginationMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllPlaceCategoriesQuery(LanguageMixin, OffsetPaginationMixin): ...
