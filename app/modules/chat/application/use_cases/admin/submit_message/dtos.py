from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitAdminMessageInputDTO:
    actor_id: UUID
    chat_id: UUID
    text: str


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitAdminMessageOutputDTO:
    message_id: UUID
