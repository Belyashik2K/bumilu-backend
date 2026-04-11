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
from app.core.enums import LanguageEnum
from app.modules.places.domain.places.models.place.exceptions import (
    PlaceIsNotEditable,
    PlaceTranslationAlreadyExists,
    PlaceTranslationNotFound,
)
from app.modules.places.domain.places.models.place_translation.model import (
    PlaceTranslation,
    PlaceTranslationData,
)
from app.modules.places.domain.places.value_objects.taxi_address.object import (
    PlaceTaxiAddressVO,
)
from app.modules.places.domain.places.value_objects.timezone.object import TimezoneVO
from app.modules.places.shared.enums.place_status import PlaceStatusEnum


@dataclass(slots=True, kw_only=True)
class Place:
    id: PlaceIdVO
    category_id: PlaceCategoryIdVO
    location: LocationVO
    timezone: TimezoneVO
    address_taxi: PlaceTaxiAddressVO
    address_taxi_comment: str | None = field(default=None)
    status: PlaceStatusEnum = field(default=PlaceStatusEnum.DRAFT)
    translation_language_codes: set[LanguageEnum] = field(default_factory=set)

    def is_draft(self) -> bool:
        return self.status == PlaceStatusEnum.DRAFT

    def is_hidden(self) -> bool:
        return self.status == PlaceStatusEnum.HIDDEN

    def is_published(self) -> bool:
        return self.status == PlaceStatusEnum.PUBLISHED

    def is_editable(self) -> bool:
        return self.is_draft() or self.is_hidden()

    @classmethod
    def create(
        cls,
        category_id: PlaceCategoryIdVO,
        location: LocationVO,
        address_taxi: PlaceTaxiAddressVO,
        address_taxi_comment: str | None = None,
    ) -> Self:
        return cls(
            id=PlaceIdVO.new(),
            category_id=category_id,
            location=location,
            timezone=TimezoneVO.from_location(location),
            address_taxi=address_taxi,
            address_taxi_comment=address_taxi_comment,
        )

    def update(
        self,
        *,
        category_id: PlaceCategoryIdVO | None = None,
        location: LocationVO | None = None,
        address_taxi: PlaceTaxiAddressVO | None = None,
        address_taxi_comment: str | None = None,
    ) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        if category_id is not None and category_id != self.category_id:
            self.category_id = category_id
        if location is not None and location != self.location:
            self.location = location
            self.timezone = TimezoneVO.from_location(location)
        if address_taxi is not None and address_taxi != self.address_taxi:
            self.address_taxi = address_taxi
        if (
            address_taxi_comment is not None
            and address_taxi_comment != self.address_taxi_comment
        ):
            self.address_taxi_comment = address_taxi_comment

    def create_translation(self, data: PlaceTranslationData) -> PlaceTranslation:
        if not self.is_editable():
            raise PlaceIsNotEditable(
                place_id=self.id,
            )

        if data.language_code in self.translation_language_codes:
            raise PlaceTranslationAlreadyExists(
                place_id=self.id,
                language_code=data.language_code,
            )

        translation = PlaceTranslation.create(
            place_id=self.id,
            data=data,
        )
        self.translation_language_codes.add(data.language_code)

        return translation

    def ensure_translation_can_be_deleted(self, language_code: LanguageEnum) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(
                place_id=self.id,
            )

        if language_code not in self.translation_language_codes:
            raise PlaceTranslationNotFound(
                place_id=self.id,
                language_code=language_code,
            )

    def remove_translation(
        self,
        language_code: LanguageEnum,
    ) -> None:
        self.ensure_translation_can_be_deleted(language_code=language_code)
        self.translation_language_codes.remove(language_code)
