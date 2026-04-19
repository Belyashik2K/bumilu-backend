from dataclasses import dataclass

from app.modules.auth.application.commands.shared_dtos import IssuedTokensDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginAsStaffMemberCommand:
    email: str
    password: str


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginAsStaffMemberCommandResult(IssuedTokensDTO): ...
