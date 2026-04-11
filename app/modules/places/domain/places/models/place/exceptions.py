from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlacePhoneIdVO,
)
from app.core.enums import LanguageEnum
from app.core.exceptions.domain.base import (
    DomainInvariantViolationException,
    DomainNotFoundException,
)
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)


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
