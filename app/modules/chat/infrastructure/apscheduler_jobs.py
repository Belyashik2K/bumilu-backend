from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler_dishka import inject
from dishka import FromDishka

from app.core.shared.utils import get_current_dt
from app.modules.chat.application.use_cases.ai.process_pending_chats import (
    ProcessPendingChatsInputDTO,
    ProcessPendingChatsUseCase,
)


@inject
async def process_pending_chats(uc: FromDishka[ProcessPendingChatsUseCase]) -> None:
    await uc(ProcessPendingChatsInputDTO())


def register_chat_jobs(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        process_pending_chats,
        trigger=IntervalTrigger(seconds=5),
        id="process_pending_chats",
        replace_existing=True,
        next_run_time=get_current_dt(),
    )
