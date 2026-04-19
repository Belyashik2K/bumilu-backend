from abc import (
    ABC,
    abstractmethod,
)
from typing import Self


class ITransactionManager(ABC):
    @abstractmethod
    async def __aenter__(self) -> Self: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
