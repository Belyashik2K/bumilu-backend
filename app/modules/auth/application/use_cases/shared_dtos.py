from dataclasses import dataclass

from app.core.shared.enums import UserRoleEnum


@dataclass(slots=True, kw_only=True, frozen=True)
class TokenInfoDTO:
    token: str
    expires_in: int


@dataclass(slots=True, kw_only=True, frozen=True)
class UserInfoDTO:
    id: str
    role: UserRoleEnum


@dataclass(slots=True, kw_only=True, frozen=True)
class IssuedTokensDTO:
    access: TokenInfoDTO
    refresh: TokenInfoDTO
    user: UserInfoDTO
