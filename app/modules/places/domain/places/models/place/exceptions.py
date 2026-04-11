from app.core.domain.value_objects.id import PlaceIdVO
from app.core.enums import LanguageEnum
from app.core.exceptions.domain.base import (
    DomainInvariantViolationException,
    DomainNotFoundException,
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
