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


class CannotPublishPlaceCategoryMissingTranslations(DomainInvariantViolationException):
    def __init__(
        self, category_id: PlaceCategoryIdVO, missing_languages: set[LanguageEnum]
    ) -> None:
        super().__init__(
            message=(
                f"Cannot publish place category with id {category_id} because it is missing translations "
                f"for languages: {', '.join(lang for lang in missing_languages)}"
            )
        )


class PlaceCategoryIsNotEditable(DomainInvariantViolationException):
    def __init__(self, category_id: PlaceCategoryIdVO) -> None:
        super().__init__(
            message=f"Place category with id {category_id} is not editable because it is published"
        )


class InvalidPlaceCategoryStatusTransition(DomainInvariantViolationException):
    def __init__(
        self,
        category_id: PlaceCategoryIdVO,
        from_status: str,
        to_status: str,
    ) -> None:
        super().__init__(
            message=(
                f"Cannot transition place category with id {category_id} from status {from_status} to {to_status}"
            )
        )
