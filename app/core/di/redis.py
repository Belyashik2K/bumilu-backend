from dishka import (
    Provider,
    Scope,
    provide,
)
from redis.asyncio import Redis

from app.core.infrastructure.config import AppConfig


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def redis_client(
        self,
        config: AppConfig,
    ) -> Redis:
        return Redis(
            username=config.redis.username,
            password=config.redis.password,
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
        )
