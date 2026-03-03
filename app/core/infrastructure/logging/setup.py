import logging
import sys

from app.core.infrastructure.logging.context import RequestIdFilter

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(request_id)s | "
    "%(name)s:%(lineno)d - "
    "%(message)s"
)


def setup_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(level)

    for handler in list(root.handlers):
        root.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, "%d.%m.%Y at %H:%M:%S"))
    handler.addFilter(RequestIdFilter())

    root.addHandler(handler)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logger = logging.getLogger(name)
        logger.handlers = []
        logger.propagate = True
