from datetime import datetime

from fastapi import Path
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.chat.shared.enums import (
    AuthorTypeEnum,
    ChatStatusEnum,
)
from app.modules.users.presentation.api.schemas.common import USER_ID_EXAMPLE

CHAT_ID_EXAMPLE = "019caaaa-0000-7000-a00a-000000001984"
MESSAGE_ID_EXAMPLE = "019caaaa-0000-7000-a00b-000000001984"
LAST_ACTIVITY_AT_EXAMPLE = "2026-03-05T04:30:00Z"

MESSAGE_TEXT_EXAMPLE = "Где Семьянов пьёт кофе?"

CHAT_ID_PATH = Path(
    ...,
    description="The unique identifier of the chat.",
    examples=[CHAT_ID_EXAMPLE],
)


class AuthorSchema(BaseModel):
    id: UUID7 | None = Field(
        None,
        description="The unique identifier of the message author.",
        examples=[USER_ID_EXAMPLE],
    )
    type: AuthorTypeEnum = Field(
        ...,
        description="The type of the message author.",
        examples=[AuthorTypeEnum.USER],
    )


class LocationSchema(BaseModel):
    latitude: float = Field(
        ...,
        description="Latitude of the user's location",
        examples=[60.0075879],
        ge=-90,
        le=90,
    )
    longitude: float = Field(
        ...,
        description="Longitude of the user's location",
        examples=[30.3735079],
        ge=-180,
        le=180,
    )


class ChatInfoSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="The unique identifier of the chat.",
        examples=[CHAT_ID_EXAMPLE],
    )
    status: ChatStatusEnum = Field(
        ...,
        description="The current status of the chat.",
        examples=[ChatStatusEnum.ACTIVE],
    )
    last_activity_at: datetime = Field(
        ...,
        description="The timestamp of the last activity in the chat.",
        examples=[LAST_ACTIVITY_AT_EXAMPLE],
    )


class ChatMessageSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="The unique identifier of the chat message.",
        examples=[MESSAGE_ID_EXAMPLE],
    )
    author: AuthorSchema = Field(
        ...,
        description="The author of the chat message.",
    )
    text: str = Field(
        ...,
        description="The text content of the chat message.",
        examples=[MESSAGE_TEXT_EXAMPLE],
        min_length=1,
        max_length=1000,
    )
    location: LocationSchema | None = Field(
        None,
        description="The geographical location associated with the message.",
    )
