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
from app.modules.chat.domain.value_objects.location import LocationVO
from app.modules.chat.shared.enums import ChatStatusEnum


@dataclass(slots=True, kw_only=True)
class Chat:
    id: ChatIdVO
    user_id: UserIdVO
    language: LanguageEnum
    status: ChatStatusEnum
    last_location: LocationVO
    last_message_preview: str | None = field(default=None)
    last_activity_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UserIdVO,
        message: str,
        language: LanguageEnum,
        location: LocationVO,
        now: datetime,
    ) -> Self:
        return cls(
            id=ChatIdVO.new(),
            user_id=user_id,
            language=language,
            status=ChatStatusEnum.ACTIVE,
            last_location=location,
            last_message_preview=message[:100],
            last_activity_at=now,
        )
