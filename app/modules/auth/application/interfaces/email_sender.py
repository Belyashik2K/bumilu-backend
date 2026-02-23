from abc import (
    ABC,
    abstractmethod,
)

from app.modules.users.domain.value_objects import EmailVO


class IEmailSender(ABC):
    @abstractmethod
    async def send(self, *, to: EmailVO, subject: str, body: str) -> None: ...
