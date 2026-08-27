from collections.abc import Iterator

import pytest
from app.modules.auth.infrastructure.stores.redis_email_challenge_store import (
    RedisEmailLoginChallengeStore,
)
from redis.asyncio import Redis
from testcontainers.community.redis import RedisContainer


@pytest.fixture(scope="module")
def redis_container() -> Iterator[RedisContainer]:
    with RedisContainer() as container:
        yield container


@pytest.fixture
async def redis_client(redis_container: RedisContainer) -> Redis:
    client = Redis(
        host=redis_container.get_container_host_ip(),
        port=int(redis_container.get_exposed_port(redis_container.port)),
    )
    await client.flushdb()
    return client


@pytest.fixture
def challenge_store(redis_client: Redis) -> RedisEmailLoginChallengeStore:
    return RedisEmailLoginChallengeStore(
        redis=redis_client,
        key_prefix="test:email-login",
    )
