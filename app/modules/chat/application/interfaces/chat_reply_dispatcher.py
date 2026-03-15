from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID


class IChatReplyDispatcher(ABC):
    @abstractmethod
    async def dispatch(
        self,
        *,
        chat_id: UUID,
        # expected_reply_version: int,
        delay_seconds: int,
    ) -> None: ...
