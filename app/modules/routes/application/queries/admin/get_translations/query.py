from dataclasses import dataclass
from uuid import UUID

from app.core.application.queries.pagination import OffsetPaginationMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminRouteTranslationsQuery(OffsetPaginationMixin):
    route_id: UUID
