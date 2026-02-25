from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.modules.auth.application.interfaces.hashers import IVerificationCodeHasher
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.interfaces.repositories.device import (
    IDeviceRepository,
)
from app.modules.auth.application.interfaces.stores.email_login import (
    IEmailLoginChallengeStore,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.application.use_cases.email.verify_code import (
    VerifyEmailCodeAtLoginInputDTO,
    VerifyEmailCodeAtLoginOutputDTO,
)
from app.modules.auth.application.use_cases.email.verify_code.exceptions import (
    InvalidEmailVerificationCode,
)
from app.modules.auth.application.use_cases.shared_dtos import (
    TokenInfoDTO,
    UserInfoDTO,
)
from app.modules.auth.domain.models.device import Device
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.domain.models.user import User
from app.modules.users.domain.value_objects import EmailVO


class VerifyEmailCodeAtLoginUseCase(
    IBaseUseCase[VerifyEmailCodeAtLoginInputDTO, VerifyEmailCodeAtLoginOutputDTO]
):
    def __init__(
        self,
        user_repository: IUserRepository,
        device_repository: IDeviceRepository,
        auth_session_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
        challenge_store: IEmailLoginChallengeStore,
        code_hasher: IVerificationCodeHasher,
    ) -> None:
        self._user_repository = user_repository
        self._device_repository = device_repository
        self._auth_session_repository = auth_session_repository
        self._auth_session_service = auth_session_service
        self._challenge_store = challenge_store
        self._code_hasher = code_hasher

    async def execute(
        self,
        input_data: VerifyEmailCodeAtLoginInputDTO,
    ) -> VerifyEmailCodeAtLoginOutputDTO:
        email = EmailVO(input_data.email)
        code = input_data.code

        code_hash = self._code_hasher.hash(email=email, code=code)
        ok = await self._challenge_store.consume(email=email, code_hash=code_hash)
        if not ok:
            raise InvalidEmailVerificationCode()

        user = await self._user_repository.get_by_email(email)
        if user is None:
            user = User.create_verified(email=email)
            await self._user_repository.save(user)

        current_device_id = DeviceIdVO(input_data.device_id)

        current_device = await self._device_repository.get_by_id(current_device_id)
        if current_device is None:
            device = Device.create(
                device_id=current_device_id,
                platform=input_data.device_platform,
                name=input_data.device_name,
                app_version=input_data.app_version,
            )
            await self._device_repository.save(device)
        else:
            await self._auth_session_repository.revoke_active_for_device(
                device_id=current_device_id
            )  # TODO: think about it, maybe remove it

        tokens = await self._auth_session_service.issue(
            user_id=user.id,
            device_id=current_device_id,
            role=user.role,
        )

        return VerifyEmailCodeAtLoginOutputDTO(
            access=TokenInfoDTO(
                token=tokens.access_token,
                expires_in=tokens.access_expires_in,
            ),
            refresh=TokenInfoDTO(
                token=tokens.refresh_token,
                expires_in=tokens.refresh_expires_in,
            ),
            user=UserInfoDTO(
                id=str(user.id),
                email=str(user.email),
                role=user.role,
            ),
        )
