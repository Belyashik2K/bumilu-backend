from dataclasses import dataclass

from app.modules.reviews.domain.value_objects.review_rating.exceptions import (
    ReviewRatingMustBeInteger,
    ReviewRatingOutOfRange,
)


@dataclass(frozen=True, slots=True)
class ReviewRatingVO:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ReviewRatingMustBeInteger(self.value)
        if not (1 <= self.value <= 5):
            raise ReviewRatingOutOfRange(self.value)

    def __str__(self) -> str:
        return str(self.value)
