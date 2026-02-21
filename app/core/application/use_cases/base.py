from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

InputDTO = TypeVar("InputDTO", contravariant=True)
OutputDTO = TypeVar("OutputDTO", covariant=True)


class IBaseUseCase(Generic[InputDTO, OutputDTO], ABC):
    @abstractmethod
    async def __call__(self, input_data: InputDTO) -> OutputDTO: ...
