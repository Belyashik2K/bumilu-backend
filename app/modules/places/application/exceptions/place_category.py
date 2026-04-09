from uuid import UUID

from app.core.enums import LanguageEnum
from app.core.exceptions.application.base import (
    ApplicationConflictException,
    ApplicationNotFoundException,
)


class PlaceCategoryAlreadyExists(ApplicationConflictException):
    def __init__(self, slug: str) -> None:
        super().__init__(message=f"Place category with slug '{slug}' already exists.")


class PlaceCategoryNotEmpty(ApplicationConflictException):
    def __init__(self, category_id: UUID, places_count: int) -> None:
        super().__init__(
            message=(
                f"Cannot delete place category with id '{category_id}' because there are "
                f"{places_count} places assigned to it."
            )
        )


class PlaceCategoryNotFound(ApplicationNotFoundException):
    def __init__(self, category_id: UUID) -> None:
        super().__init__(message=f"Place category with id '{category_id}' not found.")


class PlaceCategoryTranslationNotFound(ApplicationNotFoundException):
    def __init__(self, category_id: UUID, language_code: LanguageEnum) -> None:
        super().__init__(
            message=(
                f"Translation for place category with id '{category_id}' and language_code "
                f"'{language_code}' not found."
            )
        )
