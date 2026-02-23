from app.core.shared.exceptions.application.base import ApplicationUnauthorizedException


class InvalidRefreshToken(ApplicationUnauthorizedException):
    def __init__(self):
        super().__init__(
            message="Invalid refresh token",
        )
