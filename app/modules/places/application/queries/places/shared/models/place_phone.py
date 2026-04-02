from dataclasses import dataclass

from app.modules.places.shared.enums import PlacePhoneTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlacePhoneReadModel:
    number: str
    type: PlacePhoneTypeEnum
    primary: bool
