from dataclasses import dataclass
from typing import Final

from app.modules.chat.domain.value_objects.message_text.exceptions import (
    MessageTextCannotBeEmpty,
    MessageTextMustBeStringOrNone,
    MessageTextTooLong,
    MessageTextTooShort,
)

MAXIMUM_PREVIEW_LENGTH: Final[int] = 32

MINIMUM_MESSAGE_LENGTH: Final[int] = 1
MAXIMUM_MESSAGE_LENGTH: Final[int] = 1000


@dataclass(frozen=True, slots=True, kw_only=True)
class MessageTextVO:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise MessageTextMustBeStringOrNone()

        prepared_value = self.value.strip()
        if prepared_value == "":
            raise MessageTextCannotBeEmpty()

        if len(self.value) < MINIMUM_MESSAGE_LENGTH:
            raise MessageTextTooShort(min_length=MINIMUM_MESSAGE_LENGTH)
        if len(self.value) > MAXIMUM_MESSAGE_LENGTH:
            raise MessageTextTooLong(max_length=MAXIMUM_MESSAGE_LENGTH)

        object.__setattr__(self, "value", prepared_value)

    @property
    def preview(self) -> str:
        if len(self.value) <= MAXIMUM_PREVIEW_LENGTH:
            return self.value
        return f"{self.value[:32]}..."
