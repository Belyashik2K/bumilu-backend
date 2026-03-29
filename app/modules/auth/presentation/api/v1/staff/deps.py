from fastapi import Depends
from starlette.requests import Request

from app.core.exceptions.application.base import (
    ApplicationForbiddenException,
    ApplicationUnauthorizedException,
)
from app.core.presentation.custom_request import CustomRequest
from app.modules.auth.presentation.api.v1.users.deps import get_principal
from app.modules.auth.shared.context import Principal


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


def get_staff_principal(request: CustomRequest) -> Principal:
    principal = get_principal(request)
    if not principal.is_staff():
        raise ApplicationForbiddenException(message="Know and fight for your rights.")
    return principal
