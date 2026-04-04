from uuid import UUID

from app.core.exceptions.application.base import ApplicationNotFoundException


class RouteNotFound(ApplicationNotFoundException):
    def __init__(self, route_id: UUID) -> None:
        super().__init__(message=f"Route with id {route_id} not found")
