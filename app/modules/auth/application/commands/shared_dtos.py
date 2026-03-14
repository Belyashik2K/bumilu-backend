from dataclasses import (
    dataclass,
)

from app.modules.users.application.queries.shared_dtos import AccountInfoDTO


@dataclass(slots=True, kw_only=True, frozen=True)
class TokenInfoDTO:
    token: str
    expires_in: int


@dataclass(slots=True, kw_only=True, frozen=True)
class IssuedTokensDTO:
    access: TokenInfoDTO
    refresh: TokenInfoDTO
    account: AccountInfoDTO
