from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceIdVO,
    PlacePhoneIdVO,
    PlacePhotoIdVO,
)
from app.core.domain.value_objects.location import LocationVO
from app.core.enums import LanguageEnum
from app.modules.places.domain.places.models.place.exceptions import (
    PlaceIsNotEditable,
    PlacePhoneAlreadyExists,
    PlacePhoneNotFound,
    PlacePhotoNotFound,
    PlaceTranslationAlreadyExists,
    PlaceTranslationNotFound,
    PlaceWorkingDayNotFound,
)
from app.modules.places.domain.places.models.place_phone.model import PlacePhone
from app.modules.places.domain.places.models.place_photo.model import PlacePhoto
from app.modules.places.domain.places.models.place_translation.model import (
    PlaceTranslation,
    PlaceTranslationData,
)
from app.modules.places.domain.places.models.place_working_day.exceptions import (
    UnsupportedPlaceWorkingDayStatus,
)
from app.modules.places.domain.places.models.place_working_day.model import (
    PlaceWorkingDay,
    PlaceWorkingDayData,
)
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)
from app.modules.places.domain.places.value_objects.taxi_address.object import (
    PlaceTaxiAddressVO,
)
from app.modules.places.domain.places.value_objects.timezone.object import TimezoneVO
from app.modules.places.domain.places.value_objects.weekday.object import WeekdayVO
from app.modules.places.shared.enums import PlacePhoneTypeEnum
from app.modules.places.shared.enums.place_status import PlaceStatusEnum
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


def make_all_working_days_unspecified() -> list[PlaceWorkingDay]:
    return [
        PlaceWorkingDay.create(
            weekday=WeekdayVO(value=weekday),
            status=PlaceWorkingDayStatusEnum.UNSPECIFIED,
            intervals=[],
        )
        for weekday in range(1, 8)
    ]


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

    phones: list[PlacePhone] | None = field(default=None)
    working_days: list[PlaceWorkingDay] | None = field(default=None)
    photos: list[PlacePhoto] | None = field(default=None)

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
            phones=[],
            working_days=make_all_working_days_unspecified(),
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

    def add_phone(
        self,
        *,
        number: PlacePhoneNumberVO,
        type: PlacePhoneTypeEnum,
        is_primary: bool = False,
    ) -> PlacePhone:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        if self._has_phone_number(number):
            raise PlacePhoneAlreadyExists(
                place_id=self.id,
                phone_number=number,
            )

        if not self.phones:
            is_primary = True

        if is_primary:
            self._drop_primary_phone()

        phone = PlacePhone.create(
            number=number,
            type=type,
            is_primary=is_primary,
        )
        self.phones.append(phone)

        return phone

    def update_phone(
        self,
        *,
        phone_id: PlacePhoneIdVO,
        number: PlacePhoneNumberVO | None = None,
        type: PlacePhoneTypeEnum | None = None,
    ) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        phone = self._get_phone(phone_id)

        if (
            number is not None
            and number != phone.number
            and self._has_phone_number(number, exclude_phone_id=phone.id)
        ):
            raise PlacePhoneAlreadyExists(
                place_id=self.id,
                phone_number=number,
            )

        phone.update(
            number=number,
            type=type,
        )

    def make_phone_primary(
        self,
        *,
        phone_id: PlacePhoneIdVO,
    ) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        target_phone = self._get_phone(phone_id)

        for phone in self.phones:
            phone.make_non_primary()

        target_phone.make_primary()

    def remove_phone(
        self,
        *,
        phone_id: PlacePhoneIdVO,
    ) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        phone = self._get_phone(phone_id)
        was_primary = phone.is_primary

        self.phones.remove(phone)

        if was_primary and self.phones:
            self.phones[0].make_primary()

    def _get_phone(self, phone_id: PlacePhoneIdVO) -> PlacePhone:
        for phone in self.phones:
            if phone.id == phone_id:
                return phone

        raise PlacePhoneNotFound(
            place_id=self.id,
            phone_id=phone_id,
        )

    def _has_phone_number(
        self,
        number: PlacePhoneNumberVO,
        *,
        exclude_phone_id: PlacePhoneIdVO | None = None,
    ) -> bool:
        return any(
            phone.number == number and phone.id != exclude_phone_id
            for phone in self.phones
        )

    def _drop_primary_phone(self) -> None:
        for phone in self.phones:
            phone.make_non_primary()

    def replace_working_day(
        self,
        data: PlaceWorkingDayData,
    ) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        day = self._get_working_day_by_weekday(data.weekday)

        mapped_funcs = {
            PlaceWorkingDayStatusEnum.UNSPECIFIED: day.replace_with_unspecified,
            PlaceWorkingDayStatusEnum.CLOSED: day.replace_with_closed,
            PlaceWorkingDayStatusEnum.ALL_DAY: day.replace_with_all_day,
            PlaceWorkingDayStatusEnum.OPEN: lambda: day.replace_with_open(
                intervals=data.intervals
            ),
        }

        func = mapped_funcs.get(data.status)
        if func is None:
            raise UnsupportedPlaceWorkingDayStatus(status=data.status)

        func()

    def _get_working_day_by_weekday(
        self,
        weekday: WeekdayVO,
    ) -> PlaceWorkingDay:
        for day in self.working_days:
            if day.weekday == weekday:
                return day

        raise PlaceWorkingDayNotFound(
            place_id=self.id,
            weekday=weekday,
        )

    def add_photo(self, *, photo_id: PlacePhotoIdVO, file_key: str) -> PlacePhoto:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        photo = PlacePhoto.create_pending(photo_id=photo_id, file_key=file_key)

        self.photos.append(photo)
        return photo

    def mark_photo_ready(
        self,
        *,
        photo_id: PlacePhotoIdVO,
        thumbnail_file_key: str | None,
    ) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        photo = self._get_photo(photo_id)
        photo.mark_ready(thumbnail_file_key=thumbnail_file_key)

    def mark_photo_uploaded(self, *, photo_id: PlacePhotoIdVO) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        photo = self._get_photo(photo_id)
        photo.mark_uploaded()

    def remove_photo(self, *, photo_id: PlacePhotoIdVO) -> None:
        if not self.is_editable():
            raise PlaceIsNotEditable(place_id=self.id)

        photo = self._get_photo(photo_id)

        self.photos.remove(photo)

    def _get_photo(self, photo_id: PlacePhotoIdVO) -> PlacePhoto:
        for photo in self.photos:
            if photo.id == photo_id:
                return photo

        raise PlacePhotoNotFound(
            place_id=self.id,
            photo_id=photo_id,
        )
