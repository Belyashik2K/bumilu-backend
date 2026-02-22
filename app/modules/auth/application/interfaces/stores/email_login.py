from abc import (
    ABC,
    abstractmethod,
)

from app.modules.users.domain.value_objects import EmailVO


class IEmailLoginChallengeStore(ABC):
    @abstractmethod
    async def save(
        self, *, email: EmailVO, code_hash: str, ttl_seconds: int
    ) -> None: ...

    @abstractmethod
    async def verify(self, *, email: EmailVO, code_hash: str) -> bool: ...

    @abstractmethod
    async def consume(self, *, email: EmailVO, code_hash: str) -> bool: ...
