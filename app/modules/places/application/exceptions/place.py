from uuid import UUID

from app.core.enums import LanguageEnum
from app.core.exceptions.application.base import (
    ApplicationConflictException,
    ApplicationNotFoundException,
)


class PlaceNotFound(ApplicationNotFoundException):
    def __init__(self, place_id: UUID) -> None:
        super().__init__(message=f"Place with id {place_id} not found")


class PlaceIsUsedInRoute(ApplicationConflictException):
    def __init__(
        self,
        place_id: UUID,
        routes_count: int,
    ) -> None:
        super().__init__(
            message=(
                f"Place with id {place_id} is used in {routes_count} routes. "
                f"Remove the place from the routes before deleting it."
            )
        )


class PlaceTranslationNotFound(ApplicationNotFoundException):
    def __init__(self, place_id: UUID, language_code: LanguageEnum) -> None:
        super().__init__(
            message=(
                f"Translation for place with id '{place_id}' and language_code "
                f"'{language_code}' not found."
            )
        )


class PlaceWorkingDayNotFound(ApplicationNotFoundException):
    def __init__(self, place_id: UUID, weekday: int) -> None:
        super().__init__(
            message=(
                f"Working day for place with id '{place_id}' and weekday "
                f"'{weekday}' not found."
            )
        )


class PlacePhotoFileNotUploaded(ApplicationNotFoundException):
    def __init__(
        self,
        place_id: UUID,
        photo_id: UUID,
        file_key: str,
    ) -> None:
        super().__init__(
            message=(f"Photo file for place with id '{place_id}' not uploaded.")
        )
