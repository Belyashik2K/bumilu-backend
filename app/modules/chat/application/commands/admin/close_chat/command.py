from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CloseChatAsAdminCommand:
    actor_id: UUID
    chat_id: UUID
