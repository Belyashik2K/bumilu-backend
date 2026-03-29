from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
    Optional,
)
from uuid import UUID

from app.modules.chat.shared.enums import ChatStatusEnum

if TYPE_CHECKING:
    from app.modules.chat.application.queries.admin.get_chat.view import AdminChatView
    from app.modules.chat.application.queries.admin.get_chat_list.view import (
        AdminChatListPage,
    )
    from app.modules.chat.application.queries.user.get_chat.view import UserChatView


class IChatReader(ABC):
    @abstractmethod
    async def get_recent_chat_by_user_id(
        self, user_id: UUID
    ) -> Optional["UserChatView"]: ...

    @abstractmethod
    async def get_admin_chat_by_id(
        self, chat_id: UUID
    ) -> Optional["AdminChatView"]: ...

    @abstractmethod
    async def list_admin_chats(
        self,
        limit: int,
        offset: int,
        status: ChatStatusEnum | None = None,
    ) -> "AdminChatListPage": ...
