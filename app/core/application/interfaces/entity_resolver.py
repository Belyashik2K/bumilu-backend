from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class ITargetChecker(ABC):
    @abstractmethod
    async def exists(self, *args: Any, **kwargs: Any) -> bool: ...
