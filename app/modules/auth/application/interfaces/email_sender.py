from abc import (
    ABC,
    abstractmethod,
)

from app.modules.users.domain.value_objects import UserEmailVO


class IEmailSender(ABC):
    @abstractmethod
    async def send(self, *, to: UserEmailVO, subject: str, body: str) -> None: ...
