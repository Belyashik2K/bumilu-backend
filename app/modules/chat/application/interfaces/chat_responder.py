from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
)

from app.modules.chat.domain.models.chat import Chat
from app.modules.chat.domain.models.chat_message import ChatMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatResponderResult:
    reply: str
    confidence: float


class IChatResponder(ABC):
    @abstractmethod
    async def generate_reply(
        self,
        chat: Chat,
        messages: list[ChatMessage],
    ) -> ChatResponderResult: ...
