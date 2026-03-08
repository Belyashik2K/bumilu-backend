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
from app.modules.chat.domain.models.chat.exceptions import ChatNotEscalatedToAdmin
from app.modules.chat.domain.models.chat_message.model import ChatMessage
from app.modules.chat.domain.value_objects.location import LocationVO
from app.modules.chat.domain.value_objects.message_text import MessageTextVO
from app.modules.chat.shared.enums import (
    ChatCloseReasonEnum,
    ChatStatusEnum,
)
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
    closed_at: datetime | None = field(default=None)
    closed_reason: ChatCloseReasonEnum | None = field(default=None)

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
        self.last_location = location or self.last_location
        return message

    def reply_as_user(
        self,
        text: MessageTextVO,
        location: LocationVO | None,
        now: datetime,
    ) -> ChatMessage:
        if not self.is_escalated():
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
        if not self.is_escalated():
            raise ChatNotEscalatedToAdmin(chat_id=self.id)
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

    def is_escalated(self) -> bool:
        return self.status == ChatStatusEnum.ESCALATED_TO_ADMIN

    def close(
        self,
        reason: ChatCloseReasonEnum,
        now: datetime,
    ) -> None:
        self.status = ChatStatusEnum.CLOSED
        self.closed_reason = reason
        self.closed_at = self.last_activity_at = now
