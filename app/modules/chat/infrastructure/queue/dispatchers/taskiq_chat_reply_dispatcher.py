from datetime import (
    datetime,
    timedelta,
)
from uuid import UUID

from app.core.infrastructure.schedulers.taskiq import redis_source
from app.core.utils import get_current_dt
from app.modules.chat.application.interfaces.chat_reply_dispatcher import (
    IChatReplyDispatcher,
)
from app.modules.chat.infrastructure.queue.tasks import answer_with_ai_task


class TaskiqChatReplyDispatcher(IChatReplyDispatcher):
    async def dispatch(
        self,
        *,
        chat_id: UUID,
        expected_last_activity_at: datetime,
        delay_seconds: int,
    ) -> None:
        await answer_with_ai_task.schedule_by_time(
            source=redis_source,
            time=get_current_dt() + timedelta(seconds=delay_seconds),
            chat_id=chat_id,
            expected_last_activity_at=expected_last_activity_at,
        )
