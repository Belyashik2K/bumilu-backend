import logging
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

from app.core.infrastructure.logging import prepare_extras
from app.core.shared.exceptions import (
    BaseApplicationException,
    BaseDomainException,
    BaseInfrastructureException,
)
from app.core.shared.exceptions.application.base import (
    ApplicationServiceUnavailableException,
    ApplicationUnexpectedException,
)
from app.core.shared.utils import (
    start_timer,
    stop_timer,
)

InputDTO = TypeVar("InputDTO", contravariant=True)
OutputDTO = TypeVar("OutputDTO", covariant=True)

logger = logging.getLogger(__name__)


def _get_extras(
    usecase_name: str,
    **kwargs,
) -> dict:
    return prepare_extras(usecase_name=usecase_name, **kwargs)


class IBaseUseCase(Generic[InputDTO, OutputDTO], ABC):
    async def __call__(self, input_data: InputDTO) -> OutputDTO:
        uc_name = self.__class__.__name__
        started_at = start_timer()

        logger.debug("usecase_started", extra=_get_extras(uc_name))

        try:
            return await self.execute(input_data)
        except (BaseDomainException, BaseApplicationException) as e:
            logger.info("usecase_expected_error", extra=_get_extras(uc_name, error=e))
            raise
        except BaseInfrastructureException as e:
            logger.exception(
                "usecase_infrastructure_error", extra=_get_extras(uc_name, error=e)
            )
            raise ApplicationServiceUnavailableException() from e
        except Exception as e:
            logger.exception(
                "usecase_unexpected_error", extra=_get_extras(uc_name, error=e)
            )
            raise ApplicationUnexpectedException() from e
        finally:
            execution_time = stop_timer(started_at)
            logger.debug(
                "usecase_finished",
                extra=_get_extras(uc_name, execution_time_ms=execution_time),
            )

    @abstractmethod
    async def execute(self, input_data: InputDTO) -> OutputDTO: ...
