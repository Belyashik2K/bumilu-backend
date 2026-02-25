from app.core.presentation.custom_request import CustomRequest
from app.modules.auth.shared.context import Principal


def get_principal(request: CustomRequest) -> Principal:
    if not request.state.principal:
        raise Exception("Unauthorized")
    return request.state.principal
