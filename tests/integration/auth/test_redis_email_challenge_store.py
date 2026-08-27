import asyncio

import pytest
from app.modules.auth.infrastructure.stores.redis_email_challenge_store import (
    RedisEmailLoginChallengeStore,
)
from app.modules.users.domain.value_objects import UserEmailVO

pytestmark = pytest.mark.integration


@pytest.fixture
def email() -> UserEmailVO:
    return UserEmailVO.from_string("someone@gmail.com")


class TestRedisEmailLoginChallengeStoreSaveWithRateLimit:
    async def test_first_save_is_not_rate_limited(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        wait_seconds = await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="hash-1",
            ttl_seconds=60,
            min_interval_seconds=30,
        )

        assert wait_seconds == 0

    async def test_second_save_within_interval_is_rate_limited(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="hash-1",
            ttl_seconds=60,
            min_interval_seconds=30,
        )

        wait_seconds = await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="hash-2",
            ttl_seconds=60,
            min_interval_seconds=30,
        )

        assert wait_seconds > 0

    async def test_rate_limited_save_does_not_overwrite_existing_challenge(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="hash-1",
            ttl_seconds=60,
            min_interval_seconds=30,
        )
        await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="hash-2",
            ttl_seconds=60,
            min_interval_seconds=30,
        )

        assert await challenge_store.consume(email=email, code_hash="hash-2") is False
        assert await challenge_store.consume(email=email, code_hash="hash-1") is True

    async def test_save_is_allowed_again_after_interval_elapses(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="hash-1",
            ttl_seconds=60,
            min_interval_seconds=1,
        )

        await asyncio.sleep(1.2)

        wait_seconds = await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="hash-2",
            ttl_seconds=60,
            min_interval_seconds=1,
        )

        assert wait_seconds == 0


class TestRedisEmailLoginChallengeStoreConsume:
    async def test_consume_with_correct_hash_succeeds(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="correct-hash",
            ttl_seconds=60,
            min_interval_seconds=30,
        )

        consumed = await challenge_store.consume(email=email, code_hash="correct-hash")

        assert consumed is True

    async def test_consume_is_one_time_use(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="correct-hash",
            ttl_seconds=60,
            min_interval_seconds=30,
        )
        await challenge_store.consume(email=email, code_hash="correct-hash")

        consumed_again = await challenge_store.consume(
            email=email, code_hash="correct-hash"
        )

        assert consumed_again is False

    async def test_consume_with_wrong_hash_fails_and_keeps_challenge(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        await challenge_store.save_with_rate_limit(
            email=email,
            code_hash="correct-hash",
            ttl_seconds=60,
            min_interval_seconds=30,
        )

        assert (
            await challenge_store.consume(email=email, code_hash="wrong-hash") is False
        )
        assert (
            await challenge_store.consume(email=email, code_hash="correct-hash") is True
        )

    async def test_consume_without_saved_challenge_returns_false(
        self,
        challenge_store: RedisEmailLoginChallengeStore,
        email: UserEmailVO,
    ) -> None:
        consumed = await challenge_store.consume(email=email, code_hash="any-hash")

        assert consumed is False
