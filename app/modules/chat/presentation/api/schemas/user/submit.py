from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.chat.presentation.api.schemas.common import (
    CHAT_ID_EXAMPLE,
    MESSAGE_ID_EXAMPLE,
    MESSAGE_TEXT_EXAMPLE,
    LocationSchema,
)


class SubmitUserMessageRequestSchema(BaseModel):
    text: str = Field(
        ...,
        description="The text of the message to be sent by the user to the chat.",
        examples=[MESSAGE_TEXT_EXAMPLE],
        min_length=1,
        max_length=1000,
    )
    location: LocationSchema | None = Field(
        None,
        description="The optional location data of the user when sending the message.",
    )


class SubmitUserMessageResponseSchema(BaseModel):
    chat_id: UUID7 = Field(
        ...,
        description="The unique identifier of the chat to which the message was sent.",
        examples=[CHAT_ID_EXAMPLE],
    )
    message_id: UUID7 = Field(
        ...,
        description="The unique identifier of the message that was sent.",
        examples=[MESSAGE_ID_EXAMPLE],
    )


class SubmitAdminMessageRequestSchema(BaseModel):
    text: str = Field(
        ...,
        description="The text of the message to be sent by the admin to the chat.",
        examples=[MESSAGE_TEXT_EXAMPLE],
        min_length=1,
        max_length=1000,
    )


class SubmitAdminMessageResponseSchema(BaseModel):
    message_id: UUID7 = Field(
        ...,
        description="The unique identifier of the message that was sent.",
        examples=[MESSAGE_ID_EXAMPLE],
    )
