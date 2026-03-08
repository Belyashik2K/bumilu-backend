from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.shared.application.queries.pagination import OffsetPagination
from app.modules.chat.application.queries.common_views import ChatMessageView


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatMessagesQuery:
    user_id: UUID
    limit: int = field(default=20)
    offset: int = field(default=0)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatMessagesQueryResult:
    chat_id: UUID | None = field(default=None)
    messages: list[ChatMessageView] = field(default_factory=list)
    pagination: OffsetPagination | None = field(default=None)
