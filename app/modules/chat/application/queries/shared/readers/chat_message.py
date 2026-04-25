from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.modules.chat.application.queries.shared.views import (
    ChatMessagesPage,
)


class IChatMessageReader(ABC):
    @abstractmethod
    async def list_messages_by_chat_id(
        self,
        chat_id: UUID,
        limit: int,
        offset: int,
        after_message_id: UUID | None = None,
    ) -> ChatMessagesPage: ...
