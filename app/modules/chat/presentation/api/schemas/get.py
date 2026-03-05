from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.chat.presentation.api.schemas.common import (
    CHAT_ID_EXAMPLE,
    ChatInfoSchema,
    ChatMessageSchema,
)


class GetChatInfoResponseSchema(BaseModel):
    active_chat: ChatInfoSchema | None = Field(
        None,
        description="The active chat for the user, if it exists. If the user has no active chat, this field will be null.",
    )


class GetChatMessagesResponseSchema(BaseModel):
    chat_id: UUID7 | None = Field(
        ...,
        description="The unique identifier of the chat for which the messages are being retrieved.",
        examples=[CHAT_ID_EXAMPLE],
    )
    messages: list[ChatMessageSchema] = Field(
        ...,
        description="A list of messages in the user's active chat.",
    )
