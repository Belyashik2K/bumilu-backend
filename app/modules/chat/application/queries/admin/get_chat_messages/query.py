from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.shared.application.queries.pagination import (
    OffsetPagination,
    OffsetPaginationMixin,
)
from app.modules.chat.application.queries.common_views import ChatMessageView


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatMessagesQuery(OffsetPaginationMixin):
    actor_id: UUID
    chat_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatMessagesQueryResult:
    chat_id: UUID | None = field(default=None)
    messages: list[ChatMessageView] = field(default_factory=list)
    pagination: OffsetPagination
