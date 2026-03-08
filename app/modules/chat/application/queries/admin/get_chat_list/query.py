from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.shared.application.queries.pagination import (
    OffsetPagination,
    OffsetPaginationMixin,
)
from app.modules.chat.application.queries.admin.get_chat_list.view import (
    AdminChatPreviewView,
)
from app.modules.chat.shared.enums import ChatStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatListQuery(OffsetPaginationMixin):
    actor_id: UUID
    status: ChatStatusEnum | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatListQueryResult:
    chats: list[AdminChatPreviewView] = field(default_factory=list)
    pagination: OffsetPagination
