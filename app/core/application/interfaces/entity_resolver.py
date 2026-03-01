from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class IEntityResolver(ABC):
    @abstractmethod
    async def resolve(self, *args: Any, **kwargs: Any) -> bool: ...
