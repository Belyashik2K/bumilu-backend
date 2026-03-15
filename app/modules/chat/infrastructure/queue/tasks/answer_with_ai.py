from uuid import UUID

from dishka.integrations.taskiq import inject

from app.core.infrastructure.queue.broker import broker


@broker.task
@inject(patch_module=True)
async def answer_with_ai_task(chat_id: UUID) -> None:
    print("New message in chat with id: ", chat_id)
