from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Generic

from app.core.application.base_handler import (
    BaseHandler,
    CommandDTO,
    ResultDTO,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class EmptyCommand: ...


empty_command = EmptyCommand()


class ICommandHandler(Generic[CommandDTO], BaseHandler, ABC):
    async def __call__(self, command: CommandDTO) -> None:
        return await self._run_with_observability(request=command, func=self.handle)

    @abstractmethod
    async def handle(self, command: CommandDTO) -> None: ...


class ICommandHandlerWithResult(Generic[CommandDTO, ResultDTO], BaseHandler, ABC):
    async def __call__(self, command: CommandDTO) -> ResultDTO:
        return await self._run_with_observability(request=command, func=self.handle)

    @abstractmethod
    async def handle(self, command: CommandDTO) -> ResultDTO: ...
