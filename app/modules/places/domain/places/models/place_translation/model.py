from dataclasses import dataclass

from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlaceTranslationIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.places.domain.places.value_objects.description.object import (
    PlaceDescriptionVO,
)
from app.modules.places.domain.places.value_objects.display_address.object import (
    PlaceDisplayAddressVO,
)
from app.modules.places.domain.places.value_objects.short_description.object import (
    PlaceShortDescriptionVO,
)
from app.modules.places.domain.places.value_objects.title.object import PlaceTitleVO


@dataclass(slots=True, kw_only=True)
class PlaceTranslationData:
    language_code: LanguageEnum
    title: PlaceTitleVO
    description: PlaceDescriptionVO
    short_description: PlaceShortDescriptionVO
    display_address: PlaceDisplayAddressVO


@dataclass(slots=True, kw_only=True)
class PlaceTranslation:
    id: PlaceTranslationIdVO
    place_id: PlaceIdVO
    data: PlaceTranslationData

    @classmethod
    def create(
        cls,
        place_id: PlaceIdVO,
        data: PlaceTranslationData,
    ) -> "PlaceTranslation":
        return cls(
            id=PlaceTranslationIdVO.new(),
            place_id=place_id,
            data=data,
        )

    def update(
        self,
        title: PlaceTitleVO | None = None,
        description: PlaceDescriptionVO | None = None,
        short_description: PlaceShortDescriptionVO | None = None,
        display_address: PlaceDisplayAddressVO | None = None,
    ) -> None:
        if title is not None and title != self.data.title:
            self.data.title = title
        if description is not None and description != self.data.description:
            self.data.description = description
        if (
            short_description is not None
            and short_description != self.data.short_description
        ):
            self.data.short_description = short_description
        if display_address is not None and display_address != self.data.display_address:
            self.data.display_address = display_address
