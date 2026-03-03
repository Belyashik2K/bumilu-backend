from collections.abc import Mapping
from typing import (
    Any,
)

from app.core.shared.exceptions.base import BaseProjectException


class BaseInfrastructureException(BaseProjectException):
    def __init__(
        self, message: str, *, context: Mapping[str, Any] | None = None
    ) -> None:
        self.context = context or {}
        super().__init__(message)
