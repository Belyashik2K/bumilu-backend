from app.core.application.use_cases.base import IBaseUseCase
from app.modules.auth.application.use_cases.login_as_guest import (
    LoginAsGuestInputDTO,
    LoginAsGuestOutputDTO,
)


class LoginAsGuestUseCase(
    IBaseUseCase[
        LoginAsGuestInputDTO,
        LoginAsGuestOutputDTO,
    ]
):
    async def __call__(self, input_data: LoginAsGuestInputDTO) -> LoginAsGuestOutputDTO:
        return LoginAsGuestOutputDTO()
