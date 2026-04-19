from uuid import UUID

from app.core.enums import LanguageEnum
from app.core.exceptions.application.base import ApplicationNotFoundException


class RouteNotFound(ApplicationNotFoundException):
    def __init__(self, route_id: UUID) -> None:
        super().__init__(message=f"Route with id {route_id} not found")


class RouteTranslationNotFound(ApplicationNotFoundException):
    def __init__(self, route_id: UUID, language_code: LanguageEnum) -> None:
        super().__init__(
            message=f"Translation for route with id {route_id} and language code {language_code} not found"
        )
