from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.modules.chat.application.queries.user.get_chat.view import UserChatView


class IChatReader(ABC):
    @abstractmethod
    async def get_active_chat_by_user_id(
        self, user_id: UUID
    ) -> UserChatView | None: ...
