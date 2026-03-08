from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.core.shared.enums import LanguageEnum
from app.modules.chat.application.queries.common_views import (
    LocationView,
    UserView,
)
from app.modules.chat.shared.enums import ChatStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminChatPreviewView:
    id: UUID
    status: ChatStatusEnum
    user: UserView
    language: LanguageEnum
    last_activity_at: datetime
    last_message_preview: str | None
    last_location: LocationView | None


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminChatListPage:
    items: list[AdminChatPreviewView]
    total: int
