from abc import (
    ABC,
    abstractmethod,
)
from datetime import datetime
from uuid import UUID


class IChatReplyDispatcher(ABC):
    @abstractmethod
    async def dispatch(
        self,
        *,
        chat_id: UUID,
        expected_last_activity_at: datetime,
        delay_seconds: int,
    ) -> None: ...
