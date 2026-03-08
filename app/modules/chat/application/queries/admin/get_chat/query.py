from dataclasses import dataclass
from uuid import UUID

from app.modules.chat.application.queries.admin.get_chat.view import AdminChatView


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatQuery:
    actor_id: UUID
    chat_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetAdminChatQueryResult(AdminChatView): ...
