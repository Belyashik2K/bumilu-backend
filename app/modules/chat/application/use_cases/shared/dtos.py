from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from app.core.shared.enums import LanguageEnum
from app.modules.chat.shared.enums import (
    AuthorTypeEnum,
    ChatStatusEnum,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatInfoDTO:
    id: UUID
    user_id: UUID
    status: ChatStatusEnum
    language: LanguageEnum
    last_activity_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatMessageInfoDTO:
    id: UUID
    author_type: AuthorTypeEnum
    author_id: UUID | None = field(default=None)
    text: str
    latitude: float | None = field(default=None)
    longitude: float | None = field(default=None)
