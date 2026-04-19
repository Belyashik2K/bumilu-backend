from datetime import datetime
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.core.infrastructure.queue.broker import broker
from app.modules.chat.application.commands.answer_with_ai.command import (
    AnswerWithAIInChatCommand,
)
from app.modules.chat.application.commands.answer_with_ai.handler import (
    AnswerWithAIInChatCommandHandler,
)


@broker.task
@inject(patch_module=True)
async def answer_with_ai_task(
    handler: FromDishka[AnswerWithAIInChatCommandHandler],
    chat_id: UUID,
    expected_last_activity_at: datetime,
) -> None:
    await handler(
        AnswerWithAIInChatCommand(
            chat_id=chat_id,
            expected_last_activity_at=expected_last_activity_at,
        )
    )
