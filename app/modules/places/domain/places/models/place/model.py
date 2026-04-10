from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceIdVO,
)
from app.core.domain.value_objects.location import LocationVO
from app.modules.places.domain.places.value_objects.address.object import AddressVO
from app.modules.places.domain.places.value_objects.timezone.object import TimezoneVO


@dataclass(slots=True, kw_only=True)
class Place:
    id: PlaceIdVO
    category_id: PlaceCategoryIdVO
    location: LocationVO
    timezone: TimezoneVO
    address_taxi: AddressVO
    address_taxi_comment: str | None = field(default=None)

    @classmethod
    def create(
        cls,
        category_id: PlaceCategoryIdVO,
        location: LocationVO,
        timezone: TimezoneVO,
        address_taxi: AddressVO,
        address_taxi_comment: str | None = None,
    ) -> Self:
        return cls(
            id=PlaceIdVO.new(),
            category_id=category_id,
            location=location,
            timezone=timezone,
            address_taxi=address_taxi,
            address_taxi_comment=address_taxi_comment,
        )
