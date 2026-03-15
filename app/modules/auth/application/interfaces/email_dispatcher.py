from abc import (
    ABC,
    abstractmethod,
)


class IEmailDispatcher(ABC):
    @abstractmethod
    async def dispatch(self, *, to: str, subject: str, body: str) -> None: ...
