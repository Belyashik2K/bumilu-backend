from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.places.shared.models.place_translation import (
    PlaceTranslationReadModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedAdminPlaceTranslationsView:
    data: list[PlaceTranslationReadModel] = field(default_factory=list)
    pagination: OffsetPagination
