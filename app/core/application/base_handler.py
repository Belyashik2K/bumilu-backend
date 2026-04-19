import logging
from collections.abc import (
    Awaitable,
    Callable,
)
from typing import (
    Any,
    TypeVar,
)

from app.core.exceptions import (
    BaseApplicationException,
    BaseDomainException,
    BaseInfrastructureException,
)
from app.core.exceptions.application.base import (
    ApplicationServiceUnavailableException,
    ApplicationUnexpectedException,
)
from app.core.utils import (
    prepare_extras,
    start_timer,
    stop_timer,
)

CommandDTO = TypeVar("CommandDTO", contravariant=True)
QueryDTO = TypeVar("QueryDTO", contravariant=True)
ResultDTO = TypeVar("ResultDTO", covariant=True)

logger = logging.getLogger(__name__)


def _get_extras(handler_name: str, **kwargs) -> dict:
    return prepare_extras(handler_name=handler_name, **kwargs)


class BaseHandler:
    async def _run_with_observability(
        self, func: Callable[[Any], Awaitable[ResultDTO]], request: Any
    ) -> ResultDTO:
        handler_name = self.__class__.__name__
        started_at = start_timer()

        logger.debug("handler_started", extra=_get_extras(handler_name))

        try:
            return await func(request)
        except (BaseDomainException, BaseApplicationException) as e:
            details = getattr(e, "details", None) or {}
            logger.debug(
                "handler_expected_error",
                extra=_get_extras(handler_name, error=e, **details),
            )
            raise
        except BaseInfrastructureException as e:
            context = getattr(e, "context", None) or {}
            logger.exception(
                "handler_infrastructure_error",
                extra=_get_extras(handler_name, error=e, **context),
            )
            raise ApplicationServiceUnavailableException() from e
        except Exception as e:
            logger.exception(
                "handler_unexpected_error",
                extra=_get_extras(handler_name, error=e),
            )
            raise ApplicationUnexpectedException() from e
        finally:
            execution_time = stop_timer(started_at)
            logger.debug(
                "handler_finished",
                extra=_get_extras(handler_name, execution_time_ms=execution_time),
            )
