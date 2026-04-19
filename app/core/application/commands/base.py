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
from app.core.application.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, slots=True, kw_only=True)
class EmptyCommand: ...


empty_command = EmptyCommand()


class BaseCommandHandler(Generic[CommandDTO, ResultDTO], BaseHandler, ABC):
    use_transaction: bool = True

    def __init__(self, transaction_manager: ITransactionManager) -> None:
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CommandDTO) -> ResultDTO:
        if self.use_transaction:
            return await self._run_with_transaction(command)
        return await self._run_without_transaction(command)

    async def _run_with_transaction(self, command: CommandDTO) -> ResultDTO:
        async with self._transaction_manager:
            return await self._run_with_observability(
                request=command,
                func=self.handle,
            )

    async def _run_without_transaction(self, command: CommandDTO) -> ResultDTO:
        return await self._run_with_observability(
            request=command,
            func=self.handle,
        )

    @abstractmethod
    async def handle(self, command: CommandDTO): ...


class ICommandHandler(BaseCommandHandler[CommandDTO, None], ABC):
    @abstractmethod
    async def handle(self, command: CommandDTO) -> None: ...


class ICommandHandlerWithResult(
    BaseCommandHandler[CommandDTO, ResultDTO],
    Generic[CommandDTO, ResultDTO],
    ABC,
):
    @abstractmethod
    async def handle(self, command: CommandDTO) -> ResultDTO: ...
