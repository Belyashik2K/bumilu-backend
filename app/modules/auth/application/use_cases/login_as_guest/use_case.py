from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.enums import UserRoleEnum
from app.modules.auth.application.interfaces.repositories.device import (
    IDeviceRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.application.use_cases.login_as_guest import (
    LoginAsGuestInputDTO,
    LoginAsGuestOutputDTO,
)
from app.modules.auth.application.use_cases.login_as_guest.dtos import (
    TokenInfoDTO,
    UserInfoDTO,
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
        auth_session_service: AuthSessionService,
    ) -> None:
        self._user_repository = user_repository
        self._device_repository = device_repository
        self._auth_session_service = auth_session_service

    async def __call__(self, input_data: LoginAsGuestInputDTO) -> LoginAsGuestOutputDTO:
        device = await self._device_repository.get_by_id(input_data.device_id)

        if device is None or not device.has_guest_user():
            if device is None:
                device = Device.create(
                    platform=input_data.device_platform,
                    name=input_data.device_name,
                    app_version=input_data.app_version,
                )

            guest_user = User.create_guest()
            device.attach_guest_user(guest_user.id)

            await self._user_repository.save(guest_user)
            device = await self._device_repository.save(device)

        assert device.guest_user_id is not None

        session = await self._auth_session_service.issue(
            user_id=device.guest_user_id,
            device_id=device.id,
            role=UserRoleEnum.GUEST,
        )

        return LoginAsGuestOutputDTO(
            access=TokenInfoDTO(
                token=session.access_token,
                expires_in=session.access_expires_in,
            ),
            refresh=TokenInfoDTO(
                token=session.refresh_token,
                expires_in=session.refresh_expires_in,
            ),
            user=UserInfoDTO(
                id=str(device.guest_user_id),
                role=UserRoleEnum.GUEST,
            ),
        )
