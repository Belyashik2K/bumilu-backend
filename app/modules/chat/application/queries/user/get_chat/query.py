from dataclasses import (
    dataclass,
)
from uuid import UUID

from app.modules.chat.application.queries.user.get_chat.view import UserChatView


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatQuery:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserActiveChatQueryResult(UserChatView): ...
