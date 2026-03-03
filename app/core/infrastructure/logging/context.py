import logging
from contextvars import ContextVar
from uuid import (
    UUID,
    uuid4,
)

request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


def generate_request_id() -> UUID:
    return uuid4()


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get() or "-"
        return True
