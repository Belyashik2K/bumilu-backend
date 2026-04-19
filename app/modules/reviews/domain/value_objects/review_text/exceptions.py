from app.core.exceptions.domain.base import DomainValidationException


class ReviewTextMustBeStringOrNone(DomainValidationException):
    def __init__(self) -> None:
        super().__init__(
            message="Review text must be a string or None",
        )


class ReviewTextCannotBeEmpty(DomainValidationException):
    def __init__(self) -> None:
        super().__init__(
            message="Review text cannot be an empty string",
        )


class ReviewTextTooShort(DomainValidationException):
    def __init__(self, min_length: int) -> None:
        super().__init__(
            message=f"Review text must be at least {min_length} characters long",
            details={"min_length": min_length},
        )


class ReviewTextTooLong(DomainValidationException):
    def __init__(self, max_length: int) -> None:
        super().__init__(
            message=f"Review text must be at most {max_length} characters long",
            details={"max_length": max_length},
        )
