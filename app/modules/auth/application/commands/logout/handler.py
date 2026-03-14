import logging

from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.core.shared.utils import prepare_extras
from app.modules.auth.application.commands.logout import (
    LogoutCommand,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService

logger = logging.getLogger(__name__)


class LogoutCommandHandler(ICommandHandler[LogoutCommand]):
    def __init__(
        self,
        auth_session_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._auth_session_repository = auth_session_repository
        self._auth_session_service = auth_session_service

    async def handle(self, command: LogoutCommand) -> None:
        token_hash = self._auth_session_service.get_token_hash(command.refresh_token)
        session = await self._auth_session_repository.get_by_refresh_token_hash(
            token_hash
        )
        if session is None or not session.is_active():
            logger.info(
                "logout_invalid_session",
                extra=prepare_extras(
                    device_id=command.device_id,
                    reason="not_found_or_inactive",
                ),
            )
            return None

        if session.is_user_session():
            if not command.device_id:
                logger.warning(
                    "logout_invalid_session",
                    extra=prepare_extras(
                        session_id=str(session.id),
                        reason="missing_device_id_for_user_session",
                    ),
                )
                return None

            current_device_id = DeviceIdVO.from_uuid(command.device_id)
            if session.device_id != current_device_id:
                logger.warning(
                    "logout_invalid_session",
                    extra=prepare_extras(
                        device_id=command.device_id,
                        session_id=str(session.id),
                        reason="device_mismatch",
                    ),
                )
                return None

        await self._auth_session_service.revoke(session=session)
        return None
