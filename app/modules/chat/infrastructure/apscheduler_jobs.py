from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler_dishka import inject
from dishka import FromDishka

from app.core.application.commands import EmptyCommand
from app.core.shared.utils import get_current_dt
from app.modules.chat.application.commands.ai import ProcessPendingChatsCommandHandler


@inject
async def process_pending_chats(
    command: FromDishka[ProcessPendingChatsCommandHandler],
) -> None:
    await command(EmptyCommand())


def register_chat_jobs(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        process_pending_chats,
        trigger=IntervalTrigger(seconds=1),
        id="process_pending_chats",
        replace_existing=True,
        next_run_time=get_current_dt(),
    )
