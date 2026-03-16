from dataclasses import (
    dataclass,
)
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserRecentChatQuery:
    user_id: UUID
