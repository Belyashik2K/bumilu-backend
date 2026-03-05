from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self

from app.core.shared.domain.value_objects.id import (
    ChatIdVO,
    UserIdVO,
)
from app.core.shared.enums import LanguageEnum
from app.modules.chat.domain.models.chat_message.model import ChatMessage
from app.modules.chat.domain.value_objects.location import LocationVO
from app.modules.chat.domain.value_objects.message_text import MessageTextVO
from app.modules.chat.shared.enums import ChatStatusEnum
from app.modules.chat.shared.enums.author_type import (
    AuthorTypeEnum,
)


@dataclass(slots=True, kw_only=True)
class Chat:
    id: ChatIdVO
    user_id: UserIdVO
    language: LanguageEnum
    status: ChatStatusEnum
    last_location: LocationVO | None = field(default=None)
    last_message_preview: MessageTextVO | None = field(default=None)
    last_activity_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UserIdVO,
        language: LanguageEnum,
        location: LocationVO | None,
        now: datetime,
    ) -> Self:
        return cls(
            id=ChatIdVO.new(),
            user_id=user_id,
            language=language,
            status=ChatStatusEnum.ACTIVE,
            last_location=location,
            last_activity_at=now,
        )

    def _add_message(
        self,
        author_id: UserIdVO | None,
        author_type: AuthorTypeEnum,
        text: MessageTextVO,
        location: LocationVO | None,
        now: datetime,
    ) -> ChatMessage:
        message = ChatMessage.create(
            chat_id=self.id,
            author_id=author_id,
            author_type=author_type,
            text=text,
            location=location,
        )
        self.last_message_preview = text
        self.last_activity_at = now
        return message

    def reply_as_user(
        self,
        text: MessageTextVO,
        location: LocationVO | None,
        now: datetime,
    ) -> ChatMessage:
        self.status = ChatStatusEnum.WAITING_FOR_AI
        return self._add_message(
            author_id=self.user_id,
            author_type=AuthorTypeEnum.USER,
            text=text,
            location=location,
            now=now,
        )

    def reply_as_admin(
        self,
        author_id: UserIdVO,
        text: MessageTextVO,
        now: datetime,
    ) -> ChatMessage:
        self.status = ChatStatusEnum.ACTIVE
        return self._add_message(
            author_id=author_id,
            author_type=AuthorTypeEnum.ADMIN,
            text=text,
            location=None,
            now=now,
        )

    def reply_as_ai(
        self,
        text: MessageTextVO,
        now: datetime,
    ) -> ChatMessage:
        self.status = ChatStatusEnum.ACTIVE
        return self._add_message(
            author_id=None,
            author_type=AuthorTypeEnum.AI,
            text=text,
            location=None,
            now=now,
        )

    def escalate_to_admin(
        self,
        now: datetime,
    ) -> None:
        self.status = ChatStatusEnum.ESCALATED_TO_ADMIN
        self.last_activity_at = now
