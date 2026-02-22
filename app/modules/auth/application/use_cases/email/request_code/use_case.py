from app.core.application.use_cases.base import IBaseUseCase
from app.modules.auth.application.use_cases.email.request_code import (
    RequestEmailCodeAtLoginInputDTO,
    RequestEmailCodeAtLoginOutputDTO,
)
from app.modules.users.domain.value_objects import EmailVO


class RequestEmailCodeAtLoginUseCase(
    IBaseUseCase[
        RequestEmailCodeAtLoginInputDTO,
        RequestEmailCodeAtLoginOutputDTO,
    ]
):
    def __init__(
        self,
    ) -> None: ...

    async def __call__(
        self,
        input_data: RequestEmailCodeAtLoginInputDTO,
    ) -> RequestEmailCodeAtLoginOutputDTO:
        email = EmailVO(input_data.email)  # noqa: F841

        return RequestEmailCodeAtLoginOutputDTO()
