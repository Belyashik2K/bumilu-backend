import logging
from typing import Final

from redis import RedisError
from redis.asyncio import Redis

from app.core.shared.utils import prepare_extras
from app.modules.auth.application.interfaces.stores.email_login import (
    IEmailLoginChallengeStore,
)
from app.modules.users.domain.value_objects import EmailVO

_CONSUME_LUA: Final[str] = """
-- KEYS[1] = key
-- ARGV[1] = expected_hash
local cur = redis.call("GET", KEYS[1])
if not cur then
  return 0
end
if cur == ARGV[1] then
  redis.call("DEL", KEYS[1])
  return 1
end
return 0
"""

_SAVE_WITH_RL_LUA: Final[str] = r"""
local challenge_key = KEYS[1]
local rl_key = KEYS[2]

local code_hash = ARGV[1]
local ttl_seconds = tonumber(ARGV[2])
local min_interval_seconds = tonumber(ARGV[3])

-- cooldown active?
local exists = redis.call("EXISTS", rl_key)
if exists == 1 then
  local ttl = redis.call("TTL", rl_key)
  if ttl < 0 then ttl = min_interval_seconds end
  return ttl
end

redis.call("SET", challenge_key, code_hash, "EX", ttl_seconds)
redis.call("SET", rl_key, "1", "EX", min_interval_seconds)
return 0
"""

logger = logging.getLogger(__name__)


class RedisEmailLoginChallengeStore(IEmailLoginChallengeStore):
    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        host: str,
        port: int,
        db: int,
        key_prefix: str,
    ) -> None:
        self._redis = Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db,
        )
        self._key_prefix = key_prefix

    def _rl_key(self, email: EmailVO) -> str:
        return f"{self._key_prefix}:rl:{email!s}"

    def _key(self, email: EmailVO) -> str:
        return f"{self._key_prefix}:{email!s}"

    async def consume(self, *, email: EmailVO, code_hash: str) -> bool:
        try:
            res = await self._redis.eval(  # type: ignore
                _CONSUME_LUA,
                1,
                self._key(email),
                code_hash,
            )
            logger.debug(
                "email_login_challenge_store_consume_result",
                extra=prepare_extras(email=email.fingerprint, success=bool(res)),
            )
        except RedisError:
            logger.exception(
                "email_login_challenge_store_consume_failed",
                extra=prepare_extras(email=email.fingerprint),
            )
            raise
        return bool(res)

    async def save_with_rate_limit(
        self,
        *,
        email: EmailVO,
        code_hash: str,
        ttl_seconds: int,
        min_interval_seconds: int,
    ) -> int:
        try:
            res = await self._redis.eval(  # type: ignore
                _SAVE_WITH_RL_LUA,
                2,
                self._key(email),
                self._rl_key(email),
                code_hash,
                str(ttl_seconds),
                str(min_interval_seconds),
            )
            logger.debug(
                "email_login_challenge_store_save_result",
                extra=prepare_extras(
                    email=email.fingerprint,
                    ttl_seconds=ttl_seconds,
                    min_interval_seconds=min_interval_seconds,
                ),
            )
            return max(int(res), 0)
        except RedisError:
            logger.exception(
                "email_login_challenge_store_save_failed",
                extra=prepare_extras(email=email.fingerprint),
            )
            raise
