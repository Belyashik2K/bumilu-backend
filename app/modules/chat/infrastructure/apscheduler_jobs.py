from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler_dishka import inject
from dishka import FromDishka

from app.core.application.commands.base import empty_command
from app.core.infrastructure.config import AppConfig
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.ai import ProcessPendingChatsCommandHandler
from app.modules.chat.application.commands.close_inactive_chats import (
    CloseInactiveChatsCommandHandler,
)


@inject
async def process_pending_chats(
    command: FromDishka[ProcessPendingChatsCommandHandler],
) -> None:
    await command(empty_command)


@inject
async def close_inactive_chats(
    command: FromDishka[CloseInactiveChatsCommandHandler],
) -> None:
    await command(empty_command)


def register_chat_jobs(
    scheduler: AsyncIOScheduler,
    config: AppConfig,
) -> None:
    now = get_current_dt()
    scheduler.add_job(
        process_pending_chats,
        trigger=IntervalTrigger(
            seconds=config.chat.ai_assistant.polling_interval_seconds
        ),
        id="process_pending_chats",
        replace_existing=True,
        next_run_time=now,
    )
    scheduler.add_job(
        close_inactive_chats,
        trigger=IntervalTrigger(
            seconds=config.chat.inactivity.polling_interval_seconds
        ),
        id="close_inactive_chats",
        replace_existing=True,
        next_run_time=now,
    )
