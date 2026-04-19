from app.core.exceptions.application.base import ApplicationUnauthorizedException


class InvalidEmailVerificationCode(ApplicationUnauthorizedException):
    def __init__(self):
        super().__init__(
            message="Verification code is invalid or expired.",
        )
