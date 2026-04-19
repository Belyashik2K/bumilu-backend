from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceUserContextReadModel:
    is_favorite: bool = field(default=False)
