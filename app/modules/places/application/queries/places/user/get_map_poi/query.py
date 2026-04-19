from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.language import LanguageMixin
from app.modules.places.application.queries.places.shared.dtos import BBox


@dataclass(frozen=True, slots=True, kw_only=True)
class GetPlacesMapPOIQuery(LanguageMixin):
    bounds: BBox
    limit: int = field(default=100)
