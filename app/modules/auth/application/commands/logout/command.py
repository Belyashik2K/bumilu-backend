from dataclasses import (
    dataclass,
)
from uuid import UUID


@dataclass(slots=True, kw_only=True, frozen=True)
class LogoutCommand:
    refresh_token: str
    device_id: UUID
