from dataclasses import dataclass

from app.core.domain.value_objects.string.object import BaseStringVO
from app.modules.places.domain.places.value_objects.taxi_address.exceptions import (
    InvalidAddress,
)

SPB_PREFIX = "Санкт-Петербург, "


@dataclass(frozen=True, slots=True)
class PlaceTaxiAddressVO(BaseStringVO):
    min_length = len(SPB_PREFIX) + 1
    max_length = 255

    @classmethod
    def additional_validate(cls, value: str) -> None:
        if not value.startswith(SPB_PREFIX):
            raise InvalidAddress(
                message=f"Address must start with '{SPB_PREFIX}'", address=value
            )

        rest = value.removeprefix(SPB_PREFIX).strip()
        if not rest:
            raise InvalidAddress(
                message="Address must contain more than just the city name",
                address=value,
            )

        return value
