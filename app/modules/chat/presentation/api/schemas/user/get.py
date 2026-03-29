from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import OffsetPaginationSchema
from app.modules.chat.presentation.api.schemas.common import (
    CHAT_ID_EXAMPLE,
    ChatInfoSchema,
    ChatMessageSchema,
)


class GetChatInfoResponseSchema(ChatInfoSchema): ...


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
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination information for the retrieved messages.",
    )
