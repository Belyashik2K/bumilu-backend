from app.core.shared.exceptions.application.base import (
    ApplicationRateLimitExceededException,
)


class VerificationCodeRequestedTooEarly(ApplicationRateLimitExceededException):
    def __init__(self, retry_after_seconds: int):
        super().__init__(
            message="Verification code requested too early",
            details={"retry_after": retry_after_seconds},
        )
