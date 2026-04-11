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


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceTranslationData:
    language_code: LanguageEnum
    title: PlaceTitleVO
    description: PlaceDescriptionVO
    short_description: PlaceShortDescriptionVO
    display_address: PlaceDisplayAddressVO


@dataclass(slots=True, kw_only=True)
class PlaceTranslation:
    id: PlaceTranslationIdVO
    category_id: PlaceIdVO
    data: PlaceTranslationData

    @classmethod
    def create(
        cls,
        category_id: PlaceIdVO,
        data: PlaceTranslationData,
    ) -> "PlaceTranslation":
        return cls(
            id=PlaceTranslationIdVO.new(),
            category_id=category_id,
            data=data,
        )
