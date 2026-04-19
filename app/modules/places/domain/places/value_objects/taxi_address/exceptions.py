from app.core.exceptions.domain.base import DomainValidationException


class InvalidAddress(DomainValidationException):
    def __init__(
        self,
        address: str,
        message: str = "Invalid address value",
    ) -> None:
        super().__init__(
            message=message,
            details={"address": address},
        )
