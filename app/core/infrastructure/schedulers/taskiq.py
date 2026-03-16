from taskiq import TaskiqScheduler
from taskiq_redis import (
    ListRedisScheduleSource,
)

from app.core.infrastructure.queue.broker import (
    broker,
    build_redis_url,
)

redis_source = ListRedisScheduleSource(build_redis_url())

scheduler = TaskiqScheduler(broker, sources=[redis_source])
