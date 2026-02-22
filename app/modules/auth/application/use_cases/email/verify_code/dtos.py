from dataclasses import dataclass
from uuid import UUID

from app.modules.auth.application.use_cases.shared_dtos import IssuedTokensDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class VerifyEmailCodeAtLoginInputDTO:
    email: str
    code: str
    device_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class VerifyEmailCodeAtLoginOutputDTO(IssuedTokensDTO): ...
