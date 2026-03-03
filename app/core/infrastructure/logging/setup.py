import logging
import sys

from app.core.infrastructure.logging.context import RequestIdFilter
from app.core.infrastructure.logging.extras import ExtraFormatter


def setup_logging(
    level: str,
    format: str,
    datefmt: str,
) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    for handler in list(root.handlers):
        root.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ExtraFormatter(format, datefmt))
    handler.addFilter(RequestIdFilter())

    root.addHandler(handler)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logger = logging.getLogger(name)
        logger.handlers = []
        logger.propagate = True

    root.info("Logging is configured with level: %s", level)
