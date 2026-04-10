from dataclasses import dataclass

from app.modules.places.domain.places.value_objects.address.exceptions import (
    InvalidAddress,
)

SPB_PREFIX = "Санкт-Петербург, "


@dataclass(frozen=True, slots=True)
class AddressVO:
    value: str

    def __post_init__(self) -> None:
        value = self.value.strip()

        if not value:
            raise InvalidAddress(message="Address cannot be empty", address=self.value)

        if len(value) > 255:
            raise InvalidAddress(
                message="Address cannot exceed 255 characters", address=value
            )

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

        object.__setattr__(self, "value", value)
