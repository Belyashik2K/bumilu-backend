from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.pagination import (
    OffsetPaginationMixin,
)
from app.modules.chat.shared.enums import ChatStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatListQuery(OffsetPaginationMixin):
    actor_id: UUID
    status: ChatStatusEnum | None = field(default=None)
