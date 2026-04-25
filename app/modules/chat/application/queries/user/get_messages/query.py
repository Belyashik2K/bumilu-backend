from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.application.queries.pagination import (
    OffsetPaginationMixin,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserRecentChatMessagesQuery(OffsetPaginationMixin):
    user_id: UUID
    after_message_id: UUID | None = field(default=None)
