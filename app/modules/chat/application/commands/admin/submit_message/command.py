from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitAdminMessageCommand:
    actor_id: UUID
    chat_id: UUID
    text: str


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitAdminMessageCommandResult:
    message_id: UUID
