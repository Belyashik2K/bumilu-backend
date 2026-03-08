from dataclasses import (
    dataclass,
)
from uuid import UUID


@dataclass(slots=True, kw_only=True, frozen=True)
class LogoutInputDTO:
    refresh_token: str
    device_id: UUID


@dataclass(slots=True, kw_only=True, frozen=True)
class LogoutOutputDTO: ...
