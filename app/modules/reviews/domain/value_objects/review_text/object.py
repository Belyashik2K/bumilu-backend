from dataclasses import dataclass
from typing import Final

from app.modules.reviews.domain.value_objects.review_text.exceptions import (
    ReviewTextCannotBeEmpty,
    ReviewTextMustBeStringOrNone,
    ReviewTextTooLong,
    ReviewTextTooShort,
)

MINIMUM_REVIEW_TEXT_LENGTH: Final[int] = 10
MAXIMUM_REVIEW_TEXT_LENGTH: Final[int] = 1000


@dataclass(frozen=True, slots=True)
class ReviewTextVO:
    value: str | None

    def __post_init__(self) -> None:
        if self.value is None:
            return

        if not isinstance(self.value, str):
            raise ReviewTextMustBeStringOrNone()

        prepared_value = self.value.strip()
        if prepared_value == "":
            raise ReviewTextCannotBeEmpty()

        review_text_length = len(prepared_value)
        if review_text_length < MINIMUM_REVIEW_TEXT_LENGTH:
            raise ReviewTextTooShort(MINIMUM_REVIEW_TEXT_LENGTH)
        if review_text_length > MAXIMUM_REVIEW_TEXT_LENGTH:
            raise ReviewTextTooLong(MAXIMUM_REVIEW_TEXT_LENGTH)

        object.__setattr__(self, "value", prepared_value)
