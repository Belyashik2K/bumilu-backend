from app.core.application.commands import (
    ICommandHandlerWithResult,
)
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.auth.application.commands.shared_dtos import TokenInfoDTO
from app.modules.auth.application.commands.staff.login import (
    LoginAsStaffMemberCommand,
    LoginAsStaffMemberCommandResult,
)
from app.modules.auth.application.commands.staff.login.exceptions import (
    InvalidCredentials,
    PrincipalNotFound,
)
from app.modules.auth.application.interfaces.hashers import IStaffPasswordHasher
from app.modules.auth.application.interfaces.repositories.principal import (
    IPrincipalRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.domain.models.principal import Principal
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.application.interfaces.repositories.staff_member import (
    IStaffMemberRepository,
)
from app.modules.staff.domain.models.staff_member import StaffMember
from app.modules.staff.domain.value_objects.staff_email import StaffMemberEmailVO
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum
from app.modules.users.application.queries.shared.dtos import AccountInfoDTO


class LoginAsStaffMemberCommandHandler(
    ICommandHandlerWithResult[
        LoginAsStaffMemberCommand, LoginAsStaffMemberCommandResult
    ],
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        principal_repository: IPrincipalRepository,
        staff_member_repository: IStaffMemberRepository,
        staff_password_hasher: IStaffPasswordHasher,
        auth_session_service: AuthSessionService,
    ) -> None:
        super().__init__(transaction_manager)
        self._principal_repository = principal_repository
        self._staff_member_repository = staff_member_repository
        self._staff_password_hasher = staff_password_hasher
        self._auth_session_service = auth_session_service

    async def handle(
        self, command: LoginAsStaffMemberCommand
    ) -> LoginAsStaffMemberCommandResult:
        staff_member_email = StaffMemberEmailVO.from_string(command.email)

        staff_member = await self._staff_member_repository.get_by_email(
            staff_member_email
        )

        if staff_member is None:
            if await self._staff_member_repository.total_staff_members() == 0:
                principal = Principal.create(type=PrincipalTypeEnum.STAFF)
                staff_member = StaffMember.create(
                    id=principal.id,
                    name="Owner",
                    email=staff_member_email,
                    password_hash=self._staff_password_hasher.hash(command.password),
                    role=StaffRoleEnum.OWNER,
                )
                await self._principal_repository.save(principal)
                await self._staff_member_repository.save(staff_member)
            else:
                raise InvalidCredentials()

        if not self._staff_password_hasher.verify(
            password=command.password, password_hash=staff_member.password_hash
        ):
            raise InvalidCredentials()

        principal = await self._principal_repository.get_by_id(staff_member.id)
        if principal is None:
            raise PrincipalNotFound()

        tokens = await self._auth_session_service.issue(
            principal=principal,
            role=staff_member.role,
        )

        return LoginAsStaffMemberCommandResult(
            access=TokenInfoDTO(
                token=tokens.access_token,
                expires_in=tokens.access_expires_in,
            ),
            refresh=TokenInfoDTO(
                token=tokens.refresh_token,
                expires_in=tokens.refresh_expires_in,
            ),
            account=AccountInfoDTO(
                id=str(staff_member.id),
                email=str(staff_member.email),
                role=staff_member.role,
            ),
        )
