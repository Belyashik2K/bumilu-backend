from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.core.shared.application.queries.pagination import (
    OffsetPaginationMixin,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatMessagesQuery(OffsetPaginationMixin):
    user_id: UUID
