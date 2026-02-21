from app.core.application.use_cases.base import IBaseUseCase
from app.modules.auth.application.interfaces.repositories.device import (
    IDeviceRepository,
)
from app.modules.auth.application.interfaces.repositories.refresh_session import (
    IRefreshSessionRepository,
)
from app.modules.auth.application.use_cases.login_as_guest import (
    LoginAsGuestInputDTO,
    LoginAsGuestOutputDTO,
)
from app.modules.auth.domain.models.device import Device
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.domain.models.user import User


class LoginAsGuestUseCase(
    IBaseUseCase[
        LoginAsGuestInputDTO,
        LoginAsGuestOutputDTO,
    ]
):
    def __init__(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        refresh_session_repository: IRefreshSessionRepository,
    ) -> None:
        self._user_repository = user_repository
        self._device_repository = device_repository
        self._refresh_session_repository = refresh_session_repository

    async def __call__(self, input_data: LoginAsGuestInputDTO) -> LoginAsGuestOutputDTO:
        device = await self._device_repository.get_by_id(input_data.device_id)

        if device and device.has_guest_user():
            guest_user_id = device.guest_user_id
        else:
            guest_user = User.create_guest()
            guest_user = await self._user_repository.save(guest_user)

            if device is None:
                device = Device.create(
                    platform=input_data.device_platform,
                    name=input_data.device_name,
                    app_version=input_data.app_version,
                )
            device.attach_guest_user(guest_user.id)
            device = await self._device_repository.save(device)
            guest_user_id = guest_user.id  # noqa: F841

        ...  # Creating refresh session and get access/refresh tokens

        return LoginAsGuestOutputDTO()
