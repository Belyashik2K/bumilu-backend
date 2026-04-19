import re
from dataclasses import dataclass

from app.core.domain.value_objects.string.object import BaseStringVO
from app.modules.places.domain.places.value_objects.phone_number.exceptions import (
    InvalidPlacePhoneNumber,
)


@dataclass(frozen=True, slots=True)
class PlacePhoneNumberVO(BaseStringVO):
    max_length = 20
    pattern = r"^[\d\+\-\s\(\)]+$"

    @classmethod
    def additional_validate(cls, value: str) -> str:
        digits = re.sub(r"\D", "", value)

        if len(digits) != 11:
            raise InvalidPlacePhoneNumber(
                f"{cls.__name__}: phone must contain 11 digits, got {len(digits)}"
            )

        if digits.startswith("8") or digits.startswith("7"):
            normalized = "+7" + digits[1:]
        else:
            raise InvalidPlacePhoneNumber(
                f"{cls.__name__}: phone must start with 7 or 8"
            )

        return normalized
