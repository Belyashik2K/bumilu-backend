from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitUserMessageCommand:
    user_id: UUID
    text: str
    latitude: float | None = field(default=None)
    longitude: float | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitUserMessageCommandResult:
    chat_id: UUID
    message_id: UUID
