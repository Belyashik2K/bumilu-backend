from app.core.exceptions.application.base import (
    ApplicationNotFoundException,
    ApplicationUnauthorizedException,
)


class InvalidCredentials(ApplicationUnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials provided.",
        )


class PrincipalNotFound(ApplicationNotFoundException):
    def __init__(self) -> None:
        super().__init__(
            message="Principal not found.",
        )
