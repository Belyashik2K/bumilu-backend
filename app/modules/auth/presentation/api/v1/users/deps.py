from app.core.presentation.custom_request import CustomRequest
from app.core.shared.exceptions.application.base import (
    ApplicationForbiddenException,
    ApplicationUnauthorizedException,
)
from app.modules.auth.shared.context import Principal


def get_principal(request: CustomRequest) -> Principal:
    if not request.state.principal:
        raise ApplicationUnauthorizedException(message="Who are you, stranger?")
    return request.state.principal


def get_user_principal(request: CustomRequest) -> Principal:
    principal = get_principal(request)
    if not principal.is_user():
        raise ApplicationForbiddenException(
            message="You're too cool for that, brother."
        )
    return request.state.principal
