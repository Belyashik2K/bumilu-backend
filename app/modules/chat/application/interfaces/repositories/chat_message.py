from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import ChatIdVO
from app.modules.chat.domain.models.chat_message import ChatMessage


class IChatMessageRepository(IBaseRepository[ChatMessage], ABC):
    @abstractmethod
    async def get_chat_messages(self, chat_id: ChatIdVO) -> list[ChatMessage]: ...
