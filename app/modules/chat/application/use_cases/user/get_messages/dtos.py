from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.chat.application.use_cases.shared.dtos import ChatMessageInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatMessagesInputDTO:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatMessagesOutputDTO:
    chat_id: UUID | None = field(default=None)
    messages: list[ChatMessageInfoDTO] = field(default_factory=list)
