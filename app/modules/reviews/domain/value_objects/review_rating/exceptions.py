from typing import Any

from app.core.exceptions.domain.base import DomainValidationException


class ReviewRatingMustBeInteger(DomainValidationException):
    def __init__(self, rating: Any) -> None:
        super().__init__(
            message="Review rating must be an integer",
            details={"rating": rating},
        )


class ReviewRatingOutOfRange(DomainValidationException):
    def __init__(self, rating: int) -> None:
        super().__init__(
            message="Review rating must be between 1 and 5",
            details={"rating": rating},
        )
