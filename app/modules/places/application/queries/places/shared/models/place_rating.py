from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceRatingReadModel:
    average: float | None = field(default=None)
    reviews_count: int = field(default=0)
