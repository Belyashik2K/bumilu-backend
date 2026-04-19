from dataclasses import dataclass

from app.modules.auth.application.commands.shared_dtos import IssuedTokensDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshStaffMemberAuthSessionCommand:
    refresh_token: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshStaffMemberAuthSessionCommandResult(IssuedTokensDTO): ...
