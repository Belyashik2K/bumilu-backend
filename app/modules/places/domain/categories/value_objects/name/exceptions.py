from app.core.exceptions.domain.base import DomainValidationException


class PlaceCategoryNameCannotBeEmpty(DomainValidationException):
    def __init__(self) -> None:
        super().__init__(message="Place category name cannot be empty")
