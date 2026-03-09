from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from app.core.shared.enums import LanguageEnum
from app.modules.chat.application.queries.common_views import (
    ChatUserView,
    LocationView,
)
from app.modules.chat.shared.enums import ChatStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminChatView:
    id: UUID
    user: ChatUserView
    status: ChatStatusEnum
    language: LanguageEnum
    created_at: datetime
    last_activity_at: datetime
    last_location: LocationView | None = field(default=None)
    closed_at: datetime | None = field(default=None)
    close_reason: str | None = field(default=None)
