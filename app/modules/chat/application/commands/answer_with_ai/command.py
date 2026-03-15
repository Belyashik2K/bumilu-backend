from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class AnswerWithAIInChatCommand:
    chat_id: UUID
    expected_last_activity_at: datetime
