from app.core.shared.exceptions.domain.base import DomainValidationException


class MessageTextMustBeStringOrNone(DomainValidationException):
    def __init__(self) -> None:
        super().__init__(
            message="Message text must be a string or None",
        )


class MessageTextCannotBeEmpty(DomainValidationException):
    def __init__(self) -> None:
        super().__init__(
            message="Message text cannot be empty.",
        )


class MessageTextTooShort(DomainValidationException):
    def __init__(
        self,
        min_length: int,
    ) -> None:
        super().__init__(
            message=f"Message text must be at least {min_length} characters long.",
            details={"min_length": min_length},
        )


class MessageTextTooLong(DomainValidationException):
    def __init__(
        self,
        max_length: int,
    ) -> None:
        super().__init__(
            message=f"Message text must be at most {max_length} characters long.",
            details={"max_length": max_length},
        )
