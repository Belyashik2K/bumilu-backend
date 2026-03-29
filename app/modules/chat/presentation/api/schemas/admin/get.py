from datetime import datetime
from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.enums import LanguageEnum
from app.core.presentation.api.schemas.pagination import (
    OffsetPaginationSchema,
)
from app.modules.chat.presentation.api.schemas.admin.common import ChatUserSchema
from app.modules.chat.presentation.api.schemas.common import (
    CHAT_ID_EXAMPLE,
    LAST_ACTIVITY_AT_EXAMPLE,
    LocationSchema,
)
from app.modules.chat.shared.enums import ChatStatusEnum


class AdminChatPreviewSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="The unique identifier of the chat.",
        examples=[CHAT_ID_EXAMPLE],
    )
    status: ChatStatusEnum = Field(
        ...,
        description="The current status of the chat.",
        examples=[ChatStatusEnum.ESCALATED_TO_ADMIN],
    )
    user: ChatUserSchema = Field(
        ...,
        description="Information about the user who initiated the chat.",
    )
    language: LanguageEnum = Field(
        ...,
        description="The language in which the chat is being conducted.",
        examples=[LanguageEnum.EN],
    )
    last_activity_at: datetime = Field(
        ...,
        description="The timestamp of the last activity in the chat, which can be a message sent or received, or a location update.",
        examples=[LAST_ACTIVITY_AT_EXAMPLE],
    )
    last_message_preview: str | None = Field(
        None,
        description="A preview of the last message in the chat, which can be used to quickly identify the content of the chat without opening it.",
    )
    last_location: LocationSchema | None = Field(
        None,
        description="The last known location of the user in the chat, which can be used to provide location-based assistance or services.",
    )


class AdminChatFilterSchema(BaseModel):
    status: ChatStatusEnum | None = Field(
        None,
        description="Filter chats by their status. If not provided, chats of all statuses will be returned.",
        examples=[ChatStatusEnum.ESCALATED_TO_ADMIN],
    )


class AdminChatListResponseSchema(BaseModel):
    chats: list[AdminChatPreviewSchema] = Field(
        ...,
        description="A list of chat previews that match the specified filters and pagination parameters.",
    )
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination information for the retrieved list of chats.",
    )


class AdminChatInfoSchema(AdminChatPreviewSchema):
    last_message_preview: str | None = Field(None, exclude=True)
    created_at: datetime = Field(
        ...,
        description="The timestamp when the chat was created.",
        examples=[LAST_ACTIVITY_AT_EXAMPLE],
    )
    closed_at: datetime | None = Field(
        None,
        description="The timestamp when the chat was closed. If the chat is still active, this will be null.",
        examples=[LAST_ACTIVITY_AT_EXAMPLE],
    )
    close_reason: str | None = Field(
        None,
        description="The reason why the chat was closed, if applicable. This can provide context for the closure of the chat, such as whether it was resolved, escalated, or closed for other reasons.",
    )


def get_admin_chat_filters(
    status: Annotated[
        ChatStatusEnum | None,
        Query(
            description="Filter chats by their status. If not provided, chats of all statuses will be returned.",
            examples=[ChatStatusEnum.ESCALATED_TO_ADMIN],
        ),
    ] = None,
) -> AdminChatFilterSchema:
    return AdminChatFilterSchema(status=status)


AdminChatFiltersDep = Annotated[AdminChatFilterSchema, Depends(get_admin_chat_filters)]
