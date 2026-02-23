from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

from app.core.shared.exceptions import (
    BaseApplicationException,
    BaseDomainException,
    BaseInfrastructureException,
)
from app.core.shared.exceptions.application.base import (
    ApplicationServiceUnavailableException,
    ApplicationUnexpectedException,
)

InputDTO = TypeVar("InputDTO", contravariant=True)
OutputDTO = TypeVar("OutputDTO", covariant=True)


class IBaseUseCase(Generic[InputDTO, OutputDTO], ABC):
    async def __call__(self, input_data: InputDTO) -> OutputDTO:
        try:
            return await self.execute(input_data)
        except (BaseDomainException, BaseApplicationException):
            raise
        except BaseInfrastructureException as infrastructure_exception:
            raise ApplicationServiceUnavailableException() from infrastructure_exception
        except Exception as unknown_exception:
            raise ApplicationUnexpectedException() from unknown_exception

    @abstractmethod
    async def execute(self, input_data: InputDTO) -> OutputDTO: ...
