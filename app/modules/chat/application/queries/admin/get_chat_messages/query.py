from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.core.shared.application.queries.pagination import (
    OffsetPaginationMixin,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatMessagesQuery(OffsetPaginationMixin):
    actor_id: UUID
    chat_id: UUID
