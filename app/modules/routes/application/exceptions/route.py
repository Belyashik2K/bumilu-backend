from uuid import UUID

from app.core.enums import LanguageEnum
from app.core.exceptions.application.base import (
    ApplicationConflictException,
    ApplicationNotFoundException,
)


class RouteNotFound(ApplicationNotFoundException):
    def __init__(self, route_id: UUID) -> None:
        super().__init__(message=f"Route with id {route_id} not found")


class RouteTranslationNotFound(ApplicationNotFoundException):
    def __init__(self, route_id: UUID, language_code: LanguageEnum) -> None:
        super().__init__(
            message=f"Translation for route with id {route_id} and language code {language_code} not found"
        )


class InvalidPlaceIds(ApplicationNotFoundException):
    def __init__(self, expected_count: int, actual_count: int) -> None:
        super().__init__(
            message=f"Some of the provided place IDs do not exist or in other status than PUBLISHED. Expected"
            f" {expected_count} "
            f"place IDs, "
            f"but found only {actual_count}"
        )


class RouteHasTooFewPointsForBuildingRoutePath(ApplicationConflictException):
    def __init__(self, route_id: UUID) -> None:
        super().__init__(
            message=f"Route with id {route_id} has too few points for building route path. At least 2 points are required."
        )
