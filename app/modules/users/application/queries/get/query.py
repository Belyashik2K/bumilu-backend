from dataclasses import dataclass
from uuid import UUID

from app.modules.users.application.queries.shared_dtos import UserInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserQuery:
    id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserQueryResult(UserInfoDTO): ...
