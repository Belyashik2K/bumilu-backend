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


@dataclass(frozen=True, slots=True, kw_only=True)
class ReviewTextVO:
    value: str | None

    def __post_init__(self) -> None:
        if self.value is None:
            return

        if isinstance(self.value, str):
            if self.value.strip() == "":
                raise ReviewTextCannotBeEmpty()

            review_text_length = len(self.value)
            if review_text_length < MINIMUM_REVIEW_TEXT_LENGTH:
                raise ReviewTextTooShort(MINIMUM_REVIEW_TEXT_LENGTH)
            if review_text_length > MAXIMUM_REVIEW_TEXT_LENGTH:
                raise ReviewTextTooLong(MAXIMUM_REVIEW_TEXT_LENGTH)

        raise ReviewTextMustBeStringOrNone()
