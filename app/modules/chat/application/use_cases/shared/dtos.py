from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.core.shared.enums import LanguageEnum
from app.modules.chat.shared.enums import ChatStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatInfoDTO:
    id: UUID
    user_id: UUID
    status: ChatStatusEnum
    language: LanguageEnum
    last_activity_at: datetime
