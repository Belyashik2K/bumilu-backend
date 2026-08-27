import logging

from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import (
    ITransactionManager,
)
from app.core.domain.value_objects.id import DeviceIdVO
from app.core.enums import UserRoleEnum
from app.core.utils import prepare_extras
from app.modules.auth.application.commands.shared_dtos import (
    AccountInfoDTO,
    TokenInfoDTO,
)
from app.modules.auth.application.commands.user.guest.login import (
    LoginAsGuestCommand,
    LoginAsGuestCommandResult,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.interfaces.repositories.device import (
    IDeviceRepository,
)
from app.modules.auth.application.interfaces.repositories.principal import (
    IPrincipalRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.domain.models.device import Device
from app.modules.auth.domain.models.principal import Principal
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.domain.models.user import User

logger = logging.getLogger(__name__)


class LoginAsGuestCommandHandler(
    ICommandHandlerWithResult[
        LoginAsGuestCommand,
        LoginAsGuestCommandResult,
    ]
):
    def __init__(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        auth_session_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
        principal_repository: IPrincipalRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._user_repository = user_repository
        self._device_repository = device_repository
        self._auth_session_repository = auth_session_repository
        self._auth_session_service = auth_session_service
        self._principal_repository = principal_repository

    async def handle(self, command: LoginAsGuestCommand) -> LoginAsGuestCommandResult:
        device_id = DeviceIdVO.from_uuid(command.device_id)
        device = await self._device_repository.get_by_id(device_id)

        if device is None:
            device = Device.create(
                device_id=device_id,
                platform=command.device_platform,
                name=command.device_name,
                app_version=command.app_version,
            )
            logger.info(
                "device_registered",
                extra=prepare_extras(
                    device_id=device.id,
                    device_platform=device.platform,
                    device_name=device.name,
                    app_version=device.app_version,
                ),
            )

        if not device.has_guest_user():
            principal = Principal.create(type=PrincipalTypeEnum.USER)
            guest_user = User.create_guest(id=principal.id)

            await self._principal_repository.save(principal)
            await self._user_repository.save(guest_user)

            device.attach_guest_user(guest_user.id)
            await self._device_repository.save(device)

            logger.info(
                "user_created_via_guest_login",
                extra=prepare_extras(
                    user_id=str(guest_user.id),
                    device_id=str(device.id),
                ),
            )
        else:
            assert (
                device.guest_user_id is not None
            ), "device.guest_user_id must be set when device.has_guest_user() is True"
            fetched_principal = await self._principal_repository.get_by_id(
                device.guest_user_id
            )
            if fetched_principal is None:
                # TODO: More friendly error
                raise RuntimeError("Guest principal not found for device")
            principal = fetched_principal

        await self._auth_session_repository.revoke_active_for_device(
            device_id=device.id
        )
        logger.info(
            "auth_sessions_revoked_for_device",
            extra=prepare_extras(device_id=device.id),
        )

        session = await self._auth_session_service.issue(
            principal=principal,
            device_id=device.id,
            role=UserRoleEnum.GUEST,
        )

        return LoginAsGuestCommandResult(
            access=TokenInfoDTO(
                token=session.access_token,
                expires_in=session.access_expires_in,
            ),
            refresh=TokenInfoDTO(
                token=session.refresh_token,
                expires_in=session.refresh_expires_in,
            ),
            account=AccountInfoDTO(
                id=str(device.guest_user_id),
                email=None,
                role=UserRoleEnum.GUEST,
            ),
        )
