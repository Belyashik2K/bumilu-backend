from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from contextvars import Token
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
)

from app.core.infrastructure.logging.context import (
    generate_request_id,
    request_id_ctx,
)
from app.core.shared.utils import (
    start_timer,
    stop_timer,
)

logger = logging.getLogger("app.access")

PATH_TO_SKIP = ("/health", "/metrics")


def _get_header(scope: dict[str, Any], name: bytes) -> str | None:
    for k, v in scope.get("headers", []):
        if k.lower() != name:
            continue
        try:
            return v.decode("latin-1")
        except Exception as e:
            logger.warning(
                "failed_to_decode_header",
                extra={
                    "header_name": name.decode("latin-1"),
                    "error_type": e.__class__.__name__,
                },
            )
            return None
    return None


def _split_first_comma(value: str | None) -> str | None:
    if not value:
        return None
    return value.split(",", 1)[0].strip() or None


def _get_client_ip(scope: dict[str, Any]) -> str:
    xff = _split_first_comma(_get_header(scope, b"x-forwarded-for"))
    if xff:
        return xff

    x_real_ip = _get_header(scope, b"x-real-ip")
    if x_real_ip:
        return x_real_ip.strip() or "-"

    client = scope.get("client")
    if client:
        return str(client[0])

    return "-"


def _get_scheme(scope: dict[str, Any]) -> str:
    return _get_header(scope, b"x-forwarded-proto") or scope.get("scheme") or "http"


def _get_host(scope: dict[str, Any]) -> str:
    return (
        _get_header(scope, b"x-forwarded-host")
        or _get_header(scope, b"host")
        or "unknown"
    )


def _with_port_if_needed(host: str, scope: dict[str, Any]) -> str:
    xf_port = _get_header(scope, b"x-forwarded-port")
    if not xf_port:
        return host
    if ":" in host:
        return host
    return f"{host}:{xf_port}"


def _get_query_string(scope: dict[str, Any]) -> str:
    qs = scope.get("query_string") or b""
    return qs.decode("latin-1") if qs else ""


def _get_path(scope: dict[str, Any]) -> str:
    root_path = scope.get("root_path") or ""
    path = scope.get("path") or ""
    return f"{root_path}{path}"


def _build_full_url(scope: dict[str, Any]) -> str:
    scheme = _get_scheme(scope)
    host = _with_port_if_needed(_get_host(scope), scope)
    path = _get_path(scope)
    query = _get_query_string(scope)

    base = f"{scheme}://{host}{path}"
    if not query:
        return base
    return f"{base}?{query}"


def _get_user_agent(scope: dict[str, Any]) -> str:
    return _get_header(scope, b"user-agent") or "-"


def _get_xff(scope: dict[str, Any]) -> str:
    return _get_header(scope, b"x-forwarded-for") or "-"


@dataclass(slots=True)
class AccessState:
    started: float = field(default_factory=start_timer)
    status_code: int = 0
    response_bytes: int = 0

    def elapsed_ms(self) -> int:
        return stop_timer(self.started)


def _update_state_from_message(state: AccessState, message: dict[str, Any]) -> None:
    msg_type = message.get("type")

    if msg_type == "http.response.start":
        state.status_code = int(message.get("status", 0))
        return

    if msg_type == "http.response.body":
        body = message.get("body") or b""
        state.response_bytes += len(body)
        return


def _is_last_body(message: dict[str, Any]) -> bool:
    if message.get("type") != "http.response.body":
        return False
    return not message.get("more_body", False)


def _should_skip_path(path: str) -> bool:
    return path in PATH_TO_SKIP


def _make_access_extras(scope: dict[str, Any], state: AccessState) -> dict[str, Any]:
    rid = request_id_ctx.get() or "-"

    return {
        "event": "http_access",
        "request_id": rid,
        "method": scope.get("method") or "-",
        "path": _get_path(scope),
        "full_url": _build_full_url(scope),
        "status_code": state.status_code,
        "elapsed_ms": state.elapsed_ms(),
        "response_bytes": state.response_bytes,
        "client_ip": _get_client_ip(scope),
        "xff": _get_xff(scope),
        "ua": _get_user_agent(scope),
    }


def _log_by_status(status_code: int, message: str, *, extra: dict[str, Any]) -> None:
    if status_code >= 500:
        logger.error(message, extra=extra)
        return
    if status_code >= 400:
        logger.info(message, extra=extra)
        return
    logger.info(message, extra=extra)


def _set_request_id_in_scope(scope: dict[str, Any]) -> Token[str | None]:
    request_id = str(generate_request_id())
    token = request_id_ctx.set(request_id)
    scope["request_id"] = request_id
    return token


class AccessLogMiddleware:
    def __init__(self, app) -> None:
        self.app = app

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        state = AccessState()
        path = _get_path(scope)
        token = _set_request_id_in_scope(scope)

        async def send_wrapper(message: dict[str, Any]) -> None:
            _update_state_from_message(state, message)
            await send(message)

            if not _is_last_body(message):
                return

            if _should_skip_path(path):
                request_id_ctx.reset(token)
                return

            extras = _make_access_extras(scope, state)
            _log_by_status(state.status_code, "http_access", extra=extras)
            request_id_ctx.reset(token)

        await self.app(scope, receive, send_wrapper)
