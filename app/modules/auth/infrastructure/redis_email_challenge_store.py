from typing import Final

from redis.asyncio import Redis

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

    def _key(self, email: EmailVO) -> str:
        return f"{self._key_prefix}:{email!s}"

    async def save(self, *, email: EmailVO, code_hash: str, ttl_seconds: int) -> None:
        await self._redis.set(self._key(email), code_hash, ex=ttl_seconds)

    async def verify(self, *, email: EmailVO, code_hash: str) -> bool:
        cur = await self._redis.get(self._key(email))
        if cur is None:
            return False
        if isinstance(cur, bytes):
            cur = cur.decode("utf-8")
        return cur == code_hash

    async def consume(self, *, email: EmailVO, code_hash: str) -> bool:
        res = await self._redis.eval(  # type: ignore
            _CONSUME_LUA,
            1,
            self._key(email),
            code_hash,
        )
        return bool(res)
