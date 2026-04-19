from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminPlacePhotosQuery:
    place_id: UUID
