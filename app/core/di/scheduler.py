from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.infrastructure.schedulers.apscheduler import init_apscheduler


class SchedulerProvider(Provider):
    @provide(scope=Scope.APP)
    async def scheduler(self) -> AsyncIOScheduler:
        return init_apscheduler()
