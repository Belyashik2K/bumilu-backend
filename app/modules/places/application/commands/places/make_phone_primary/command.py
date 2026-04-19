from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class MakePlacePhonePrimaryCommand:
    place_id: UUID
    phone_id: UUID
