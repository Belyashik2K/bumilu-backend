from dataclasses import dataclass
from uuid import UUID

from app.core.application.queries.pagination import OffsetPaginationMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminPlaceTranslationsQuery(OffsetPaginationMixin):
    place_id: UUID
