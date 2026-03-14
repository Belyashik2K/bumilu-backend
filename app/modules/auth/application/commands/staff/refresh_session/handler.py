from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.auth.application.commands.shared_dtos import TokenInfoDTO
from app.modules.auth.application.commands.staff.refresh_session.command import (
    RefreshStaffMemberAuthSessionCommand,
    RefreshStaffMemberAuthSessionCommandResult,
)
from app.modules.auth.application.commands.user.refresh_session.exceptions import (
    InvalidRefreshToken,
)
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.application.repositories.staff import IStaffMemberRepository
from app.modules.users.application.queries.shared_dtos import AccountInfoDTO


class RefreshStaffMemberAuthSessionCommandHandler(
    ICommandHandlerWithResult[
        RefreshStaffMemberAuthSessionCommand, RefreshStaffMemberAuthSessionCommandResult
    ]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        auth_session_repository: IAuthSessionRepository,
        staff_member_repository: IStaffMemberRepository,
        auth_session_service: AuthSessionService,
    ) -> None:
        super().__init__(transaction_manager)
        self._auth_session_repository = auth_session_repository
        self._staff_member_repository = staff_member_repository
        self._auth_session_service = auth_session_service

    async def handle(
        self, command: RefreshStaffMemberAuthSessionCommand
    ) -> RefreshStaffMemberAuthSessionCommandResult:
        token_hash = self._auth_session_service.get_token_hash(command.refresh_token)

        session = await self._auth_session_repository.get_by_refresh_token_hash(
            token_hash
        )

        if session is None:
            raise InvalidRefreshToken()

        if not session.is_active():
            raise InvalidRefreshToken()

        if session.principal_type != PrincipalTypeEnum.STAFF:
            raise InvalidRefreshToken()

        staff_member = await self._staff_member_repository.get_by_id(
            session.principal_id
        )
        if staff_member is None:
            raise InvalidRefreshToken()

        new_tokens = await self._auth_session_service.rotate(
            session=session,
            role=staff_member.role,
        )

        return RefreshStaffMemberAuthSessionCommandResult(
            access=TokenInfoDTO(
                token=new_tokens.access_token,
                expires_in=new_tokens.access_expires_in,
            ),
            refresh=TokenInfoDTO(
                token=new_tokens.refresh_token,
                expires_in=new_tokens.refresh_expires_in,
            ),
            account=AccountInfoDTO(
                id=str(staff_member.id),
                email=str(staff_member.email),
                role=staff_member.role,
            ),
        )
