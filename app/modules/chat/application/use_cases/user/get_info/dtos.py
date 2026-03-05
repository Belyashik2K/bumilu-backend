from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.chat.application.use_cases.shared.dtos import ChatInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatInfoInputDTO:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatInfoOutputDTO:
    active_chat: ChatInfoDTO | None = field(default=None)
