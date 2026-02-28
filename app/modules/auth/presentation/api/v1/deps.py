from app.core.presentation.custom_request import CustomRequest
from app.core.shared.exceptions.application.base import ApplicationUnauthorizedException
from app.modules.auth.shared.context import Principal


def get_principal(request: CustomRequest) -> Principal:
    if not request.state.principal:
        raise ApplicationUnauthorizedException(message="Unauthorized")
    return request.state.principal
