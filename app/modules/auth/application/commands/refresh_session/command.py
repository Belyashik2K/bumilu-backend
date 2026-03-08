from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.modules.auth.application.commands.shared_dtos import IssuedTokensDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshAuthSessionCommand:
    refresh_token: str
    device_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshAuthSessionCommandResult(IssuedTokensDTO): ...
