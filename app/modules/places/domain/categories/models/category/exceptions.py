from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.core.enums import LanguageEnum
from app.core.exceptions.domain.base import (
    DomainConflictException,
    DomainInvariantViolationException,
    DomainNotFoundException,
)


class PlaceCategoryTranslationNotFound(DomainNotFoundException):
    def __init__(
        self, category_id: PlaceCategoryIdVO, language_code: LanguageEnum
    ) -> None:
        super().__init__(
            message=(
                f"Translation for place category with id {category_id} and language {language_code} not found"
            )
        )


class PlaceCategoryTranslationAlreadyExists(DomainConflictException):
    def __init__(
        self, category_id: PlaceCategoryIdVO, language_code: LanguageEnum
    ) -> None:
        super().__init__(
            message=f"Translation for place category with id {category_id} already exists for language {language_code}",
        )


class CannotDeleteOnlyPlaceCategoryTranslation(DomainInvariantViolationException):
    def __init__(
        self, category_id: PlaceCategoryIdVO, language_code: LanguageEnum
    ) -> None:
        super().__init__(
            message=f"Cannot delete the only translation for place category with id {category_id} and language {language_code}",
        )


class PlaceCategoryMustHaveAtLeastOneTranslation(DomainInvariantViolationException):
    def __init__(self) -> None:
        super().__init__(
            message="Place category must have at least one translation",
        )


class DuplicatePlaceCategoryTranslationLanguageCodes(DomainInvariantViolationException):
    def __init__(self, language_codes: list[LanguageEnum]) -> None:
        super().__init__(
            "Translation language codes must be unique",
            details={"language_codes": language_codes},
        )
