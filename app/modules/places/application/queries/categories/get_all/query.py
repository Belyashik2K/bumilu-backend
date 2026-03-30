from dataclasses import dataclass

from app.core.application.queries.pagination import OffsetPaginationMixin
from app.core.enums import LanguageEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAllPlaceCategoriesQuery(OffsetPaginationMixin):
    language: LanguageEnum
