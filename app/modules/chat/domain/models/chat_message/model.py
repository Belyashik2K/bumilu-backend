from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from app.core.shared.domain.value_objects.id import (
    ChatIdVO,
    ChatMessageIdVO,
    UserIdVO,
)
from app.modules.chat.domain.value_objects.location import LocationVO
from app.modules.chat.domain.value_objects.message_text import MessageTextVO
from app.modules.chat.shared.enums.author_type import AuthorTypeEnum


@dataclass(slots=True, kw_only=True)
class ChatMessage:
    id: ChatMessageIdVO
    chat_id: ChatIdVO
    author_type: AuthorTypeEnum
    author_id: UserIdVO | None = field(default=None)
    text: MessageTextVO
    location: LocationVO | None = field(default=None)

    @classmethod
    def create(
        cls,
        chat_id: ChatIdVO,
        author_type: AuthorTypeEnum,
        author_id: UserIdVO | None,
        text: MessageTextVO,
        location: LocationVO | None,
    ) -> Self:
        return cls(
            id=ChatMessageIdVO.new(),
            chat_id=chat_id,
            author_type=author_type,
            author_id=author_id,
            text=text,
            location=location,
        )
