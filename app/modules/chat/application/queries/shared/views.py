from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
from app.core.enums import UserRoleEnum
from app.modules.chat.shared.enums import AuthorTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatUserView:
    id: UUID
    email: str | None = field(default=None)
    role: UserRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatMessageAuthorView:
    type: AuthorTypeEnum
    id: UUID | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class LocationView:
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatMessageView:
    id: UUID
    author: ChatMessageAuthorView
    text: str
    location: LocationView | None = field(default=None)
    created_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatMessagesPage:
    items: list[ChatMessageView]
    total: int


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedChatMessagesView:
    chat_id: UUID | None = field(default=None)
    messages: list[ChatMessageView] = field(default_factory=list)
    pagination: OffsetPagination
