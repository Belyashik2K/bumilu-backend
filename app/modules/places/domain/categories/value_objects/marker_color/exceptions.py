from app.core.exceptions.domain.base import DomainValidationException


class InvalidMarkerColor(DomainValidationException):
    def __init__(self, color: str) -> None:
        super().__init__(
            message=f"Invalid marker color: {color}. Must be a valid hex color code (e.g., #RRGGBB).",
            details={"color": color},
        )
