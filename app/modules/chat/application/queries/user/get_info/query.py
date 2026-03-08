from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.chat.application.shared.dtos import ChatInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatInfoQuery:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatInfoQueryResult:
    active_chat: ChatInfoDTO | None = field(default=None)
