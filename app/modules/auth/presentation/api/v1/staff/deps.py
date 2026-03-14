from fastapi import Depends
from starlette.requests import Request

from app.core.shared.exceptions.application.base import ApplicationUnauthorizedException


def get_cookie_refresh_token(
    request: Request,
) -> str | None:
    return request.cookies.get("bumilu")


def require_cookie_refresh_token(
    token: str | None = Depends(get_cookie_refresh_token),
) -> str:
    if not token:
        raise ApplicationUnauthorizedException(message="Who are you, stranger?")
    return token
