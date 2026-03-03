import logging

RESERVED = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "asctime",
    "request_id",
}


def prepare_extras(**kwargs) -> dict:
    extras = {}
    for key, value in kwargs.items():
        if isinstance(value, Exception):
            extras[key] = type(value).__name__
        else:
            extras[key] = value
    return extras


class ExtraFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)

        extras = {
            k: v
            for k, v in record.__dict__.items()
            if k not in RESERVED and not k.startswith("_")
        }

        if extras:
            extra_str = " ".join(f"{k}={v}" for k, v in sorted(extras.items()))
            return f"{base} | {extra_str}"

        return base
