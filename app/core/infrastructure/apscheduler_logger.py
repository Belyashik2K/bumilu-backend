import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def create_apscheduler_logger() -> AsyncIOScheduler:
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)

    scheduler = AsyncIOScheduler()
    return scheduler
