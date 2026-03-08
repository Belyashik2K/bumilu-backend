import logging

from app.core.application.commands import ICommandHandlerWithResult
from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.core.shared.utils import prepare_extras
from app.modules.auth.application.commands.refresh_session import (
    RefreshAuthSessionCommand,
    RefreshAuthSessionCommandResult,
)
from app.modules.auth.application.commands.refresh_session.exceptions import (
    InvalidRefreshToken,
)
from app.modules.auth.application.commands.shared_dtos import (
    TokenInfoDTO,
    UserInfoDTO,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.users.application.interfaces.repositories.user import IUserRepository

logger = logging.getLogger(__name__)


class RefreshAuthSessionCommandHandler(
    ICommandHandlerWithResult[
        RefreshAuthSessionCommand,
        RefreshAuthSessionCommandResult,
    ]
):
    def __init__(
        self,
        auth_session_repository: IAuthSessionRepository,
        user_repository: IUserRepository,
        auth_session_service: AuthSessionService,
    ) -> None:
        self._auth_session_repository = auth_session_repository
        self._user_repository = user_repository
        self._auth_session_service = auth_session_service

    async def handle(
        self,
        command: RefreshAuthSessionCommand,
    ) -> RefreshAuthSessionCommandResult:
        token_hash = self._auth_session_service.get_token_hash(command.refresh_token)

        session = await self._auth_session_repository.get_by_refresh_token_hash(
            token_hash
        )

        if session is None or not session.is_active():
            logger.info(
                "refresh_invalid_session",
                extra=prepare_extras(
                    device_id=command.device_id,
                    reason="not_found_or_inactive",
                ),
            )
            raise InvalidRefreshToken()

        current_device_id = DeviceIdVO.from_uuid(command.device_id)
        if session.device_id != current_device_id:
            logger.warning(
                "refresh_invalid_session",
                extra=prepare_extras(
                    device_id=command.device_id,
                    session_id=str(session.id),
                    reason="device_mismatch",
                ),
            )
            raise InvalidRefreshToken()

        user = await self._user_repository.get_by_id(session.user_id)
        if user is None:
            logger.warning(
                "refresh_user_not_found",
                extra=prepare_extras(
                    user_id=str(session.user_id),
                    session_id=str(session.id),
                    device_id=command.device_id,
                ),
            )
            raise InvalidRefreshToken()

        new_tokens = await self._auth_session_service.rotate(
            session=session,
            role=user.role,
        )

        return RefreshAuthSessionCommandResult(
            access=TokenInfoDTO(
                token=new_tokens.access_token,
                expires_in=new_tokens.access_expires_in,
            ),
            refresh=TokenInfoDTO(
                token=new_tokens.refresh_token,
                expires_in=new_tokens.refresh_expires_in,
            ),
            user=UserInfoDTO(
                id=str(user.id),
                email=str(user.email) if user.email is not None else None,
                role=user.role,
            ),
        )
