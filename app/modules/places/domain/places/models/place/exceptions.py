from collections.abc import Collection

from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhoneIdVO,
    PlacePhotoIdVO,
)
from app.core.enums import LanguageEnum
from app.core.exceptions.domain.base import (
    DomainInvariantViolationException,
    DomainNotFoundException,
)
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)
from app.modules.places.domain.places.value_objects.weekday.object import WeekdayVO
from app.modules.places.shared.enums.place_status import PlaceStatusEnum


class PlaceIsNotEditable(DomainInvariantViolationException):
    def __init__(self, place_id: PlaceIdVO) -> None:
        super().__init__(
            message=f"Place with id {place_id} is not editable because it is published"
        )


class PlaceTranslationAlreadyExists(DomainInvariantViolationException):
    def __init__(self, place_id: PlaceIdVO, language_code: LanguageEnum) -> None:
        super().__init__(
            message=f"Translation for place with id {place_id} already exists for language {language_code}",
        )


class PlaceTranslationNotFound(DomainNotFoundException):
    def __init__(self, place_id: PlaceIdVO, language_code: LanguageEnum) -> None:
        super().__init__(
            message=f"Translation for place with id {place_id} not found for language {language_code}",
        )


class PlacePhoneAlreadyExists(DomainInvariantViolationException):
    def __init__(self, place_id: PlaceIdVO, phone_number: PlacePhoneNumberVO) -> None:
        super().__init__(
            message=f"Phone with number {phone_number} already exists for place with id {place_id}",
        )


class PlacePhoneNotFound(DomainNotFoundException):
    def __init__(self, place_id: PlaceIdVO, phone_id: PlacePhoneIdVO) -> None:
        super().__init__(
            message=f"Phone with id {phone_id} not found for place with id {place_id}",
        )


class PlaceWorkingDayNotFound(DomainNotFoundException):
    def __init__(self, place_id: PlaceIdVO, weekday: WeekdayVO) -> None:
        super().__init__(
            message=f"Working day with day_of_week {weekday} not found for place with id {place_id}",
        )


class PlacePhotoNotFound(DomainNotFoundException):
    def __init__(self, place_id: PlaceIdVO, photo_id: PlacePhotoIdVO) -> None:
        super().__init__(
            message=f"Photo with id {photo_id} not found for place with id {place_id}",
        )


class CannotPublishPlaceMissingTranslations(DomainInvariantViolationException):
    def __init__(
        self,
        place_id: PlaceIdVO,
        missing_languages: Collection[LanguageEnum],
    ) -> None:
        super().__init__(
            message=f"Cannot publish place with id {place_id} because it has missing translations for languages: "
            f"{', '.join(missing_languages)}",
        )


class InvalidPlaceStatusTransition(DomainInvariantViolationException):
    def __init__(
        self,
        place_id: PlaceIdVO,
        from_status: PlaceStatusEnum,
        to_status: PlaceStatusEnum,
    ) -> None:
        super().__init__(
            message=f"Cannot change status of place with id {place_id} from {from_status} to {to_status}",
        )
