from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler_dishka import inject
from dishka import FromDishka

from app.core.application.commands.base import empty_command
from app.core.infrastructure.config import AppConfig
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.cron import (
    CloseInactiveChatsCommandHandler,
)


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
        close_inactive_chats,
        trigger=IntervalTrigger(seconds=config.chat.inactivity.polling_interval_sec),
        id="close_inactive_chats",
        replace_existing=True,
        next_run_time=now,
    )
