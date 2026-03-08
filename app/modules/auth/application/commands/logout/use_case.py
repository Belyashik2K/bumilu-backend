import logging

from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.core.shared.utils import prepare_extras
from app.modules.auth.application.commands.logout import (
    LogoutInputDTO,
    LogoutOutputDTO,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService

logger = logging.getLogger(__name__)


class LogoutUseCase(IBaseUseCase[LogoutInputDTO, LogoutOutputDTO]):
    def __init__(
        self,
        auth_session_repository: IAuthSessionRepository,
        auth_session_service: AuthSessionService,
    ) -> None:
        self._auth_session_repository = auth_session_repository
        self._auth_session_service = auth_session_service

    async def execute(
        self,
        input_data: LogoutInputDTO,
    ) -> LogoutOutputDTO:
        output = LogoutOutputDTO()

        token_hash = self._auth_session_service.get_token_hash(input_data.refresh_token)
        session = await self._auth_session_repository.get_by_refresh_token_hash(
            token_hash
        )
        if session is None or not session.is_active():
            logger.info(
                "logout_invalid_session",
                extra=prepare_extras(
                    device_id=input_data.device_id,
                    reason="not_found_or_inactive",
                ),
            )
            return output

        current_device_id = DeviceIdVO.from_uuid(input_data.device_id)
        if session.device_id != current_device_id:
            logger.warning(
                "logout_invalid_session",
                extra=prepare_extras(
                    device_id=input_data.device_id,
                    session_id=str(session.id),
                    reason="device_mismatch",
                ),
            )
            return output

        await self._auth_session_service.revoke(session=session)

        return output
