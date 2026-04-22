from dataclasses import dataclass
from uuid import UUID

from app.core.application.queries.language import LanguageMixin


@dataclass(frozen=True, slots=True, kw_only=True)
class AddRoutePointCommand(LanguageMixin):
    route_id: UUID
    place_id: UUID
