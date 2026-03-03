import logging
from collections.abc import Callable, Coroutine, Mapping
from functools import wraps
from typing import (
    Any,
    ParamSpec,
    TypeVar,
)

from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)

from app.core.shared.exceptions import BaseInfrastructureException

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


class DatabaseIntegrityException(BaseInfrastructureException):
    def __init__(self, context: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message="Database integrity error occurred",
            context=context,
        )


class DatabaseConnectionException(BaseInfrastructureException):
    def __init__(self, context: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message="Database connection error occurred",
            context=context,
        )


def sqlalchemy_exception_catcher(
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            raise DatabaseIntegrityException() from e
        except SQLAlchemyError as e:
            raise DatabaseConnectionException() from e

    return wrapper
