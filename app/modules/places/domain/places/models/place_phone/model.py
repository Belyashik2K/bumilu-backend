from dataclasses import dataclass
from typing import Self

from app.core.domain.value_objects.id import PlacePhoneIdVO
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)
from app.modules.places.shared.enums import PlacePhoneTypeEnum


@dataclass(slots=True, kw_only=True)
class PlacePhone:
    id: PlacePhoneIdVO
    number: PlacePhoneNumberVO
    type: PlacePhoneTypeEnum
    is_primary: bool = False

    @classmethod
    def create(
        cls,
        *,
        number: PlacePhoneNumberVO,
        type: PlacePhoneTypeEnum,
        is_primary: bool = False,
    ) -> Self:
        return cls(
            id=PlacePhoneIdVO.new(),
            number=number,
            type=type,
            is_primary=is_primary,
        )

    def update(
        self,
        *,
        number: PlacePhoneNumberVO | None = None,
        type: PlacePhoneTypeEnum | None = None,
    ) -> None:
        if number is not None and number != self.number:
            self.number = number
        if type is not None and type != self.type:
            self.type = type

    def make_primary(self) -> None:
        self.is_primary = True

    def make_non_primary(self) -> None:
        self.is_primary = False
