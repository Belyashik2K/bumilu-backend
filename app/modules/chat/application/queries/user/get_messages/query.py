from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.core.shared.application.queries.pagination import (
    OffsetPaginationMixin,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserRecentChatMessagesQuery(OffsetPaginationMixin):
    user_id: UUID
