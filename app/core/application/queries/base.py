from abc import (
    ABC,
    abstractmethod,
)
from typing import Generic

from app.core.application.base_handler import (
    BaseHandler,
    QueryDTO,
    ResultDTO,
)


class IQueryHandler(Generic[QueryDTO, ResultDTO], BaseHandler, ABC):
    async def __call__(self, query: QueryDTO) -> ResultDTO:
        return await self._run_with_observability(request=query, func=self.handle)

    @abstractmethod
    async def handle(self, query: QueryDTO) -> ResultDTO: ...
