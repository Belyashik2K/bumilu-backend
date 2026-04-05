from app.core.exceptions.application.base import ApplicationConflictException


class PlaceCategoryAlreadyExists(ApplicationConflictException):
    def __init__(self, slug: str) -> None:
        super().__init__(message=f"Place category with slug '{slug}' already exists.")
