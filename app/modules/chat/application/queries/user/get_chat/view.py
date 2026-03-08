from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.chat.shared.enums import ChatStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class UserChatView:
    id: UUID
    status: ChatStatusEnum
    last_activity_at: datetime
