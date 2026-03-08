from abc import (
    ABC,
    abstractmethod,
)
from datetime import (
    datetime,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import (
    ChatIdVO,
    UserIdVO,
)
from app.modules.chat.domain.models.chat import Chat


class IChatRepository(IBaseRepository[Chat], ABC):
    @abstractmethod
    async def find_active_chat(self, user_id: UserIdVO) -> Chat | None: ...

    @abstractmethod
    async def get_active_chat_id(self, user_id: UserIdVO) -> ChatIdVO | None: ...

    @abstractmethod
    async def get_pending_chats(self) -> list[Chat]: ...

    @abstractmethod
    async def get_inactive_open_chats(self, threshold: datetime) -> list[Chat]: ...
