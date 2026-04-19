from dataclasses import dataclass

from app.core.domain.value_objects.string.object import BaseStringVO


@dataclass(frozen=True, slots=True)
class PlaceDisplayAddressVO(BaseStringVO):
    min_length = 1
    max_length = 255
