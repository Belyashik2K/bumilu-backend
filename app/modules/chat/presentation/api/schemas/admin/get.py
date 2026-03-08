from datetime import datetime

from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.shared.enums import LanguageEnum
from app.core.shared.presentation.schemas.pagination import (
    OffsetPaginationSchema,
)
from app.modules.chat.presentation.api.schemas.admin.common import ChatUserSchema
from app.modules.chat.presentation.api.schemas.common import LocationSchema
from app.modules.chat.shared.enums import ChatStatusEnum


class AdminChatPreviewSchema(BaseModel):
    id: UUID7
    status: ChatStatusEnum
    user: ChatUserSchema
    language: LanguageEnum
    last_activity_at: datetime
    last_message_preview: str | None
    last_location: LocationSchema | None


class AdminChatFilterSchema(BaseModel):
    status: ChatStatusEnum | None = Field(
        None,
        description="Filter chats by their status. If not provided, chats of all statuses will be returned.",
        examples=[ChatStatusEnum.ESCALATED_TO_ADMIN],
    )


class AdminChatListResponseSchema(BaseModel):
    chats: list[AdminChatPreviewSchema]
    pagination: OffsetPaginationSchema
