from app.core.exceptions.domain.base import DomainValidationException


class InvalidLatitude(DomainValidationException):
    def __init__(
        self,
        latitude: float,
        min_value: float = -90,
        max_value: float = 90,
    ) -> None:
        super().__init__(
            message=f"Invalid latitude value (must be between {min_value} and {max_value})",
            details={"latitude": latitude},
        )


class InvalidLongitude(DomainValidationException):
    def __init__(
        self,
        longitude: float,
        min_value: float = -180,
        max_value: float = 180,
    ) -> None:
        super().__init__(
            message=f"Invalid longitude value (must be between {min_value} and {max_value})",
            details={"longitude": longitude},
        )
