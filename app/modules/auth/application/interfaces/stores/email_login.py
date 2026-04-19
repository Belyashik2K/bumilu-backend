from abc import (
    ABC,
    abstractmethod,
)

from app.modules.users.domain.value_objects import UserEmailVO


class IEmailLoginChallengeStore(ABC):
    @abstractmethod
    async def consume(self, *, email: UserEmailVO, code_hash: str) -> bool: ...

    @abstractmethod
    async def save_with_rate_limit(
        self,
        *,
        email: UserEmailVO,
        code_hash: str,
        ttl_seconds: int,
        min_interval_seconds: int,
    ) -> int: ...
