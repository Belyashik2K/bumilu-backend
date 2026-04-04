from uuid import UUID

from app.core.exceptions.application.base import ApplicationNotFoundException


class PlaceNotFound(ApplicationNotFoundException):
    def __init__(self, place_id: UUID) -> None:
        super().__init__(message=f"Place with id {place_id} not found")
