from datetime import time

from app.core.exceptions.domain.base import DomainValidationException


class InvalidWorkingInterval(DomainValidationException):
    def __init__(
        self,
        start_time: time,
        end_time: time,
    ) -> None:
        super().__init__(
            message=f"Invalid working interval. Start time '{start_time}' must be before end time '{end_time}'."
        )
