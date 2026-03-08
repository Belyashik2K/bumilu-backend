from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.chat.application.shared.dtos import ChatMessageInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatMessagesQuery:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatMessagesQueryResult:
    chat_id: UUID | None = field(default=None)
    messages: list[ChatMessageInfoDTO] = field(default_factory=list)
