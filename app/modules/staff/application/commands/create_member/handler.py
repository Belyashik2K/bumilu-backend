from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.auth.application.interfaces.hashers import IStaffPasswordHasher
from app.modules.auth.application.interfaces.repositories.principal import (
    IPrincipalRepository,
)
from app.modules.auth.domain.models.principal import Principal
from app.modules.auth.shared.enums import PrincipalTypeEnum
from app.modules.staff.application.commands.create_member.command import (
    CreateStaffMemberCommand,
)
from app.modules.staff.application.exceptions.staff_member import (
    StaffMemberWithGivenEmailAlreadyExists,
)
from app.modules.staff.application.interfaces.repositories.staff_member import (
    IStaffMemberRepository,
)
from app.modules.staff.domain.models.staff_member import StaffMember
from app.modules.staff.domain.value_objects.staff_email import StaffMemberEmailVO
from app.modules.staff.domain.value_objects.staff_password.object import (
    StaffMemberPasswordVO,
)


class CreateStaffMemberCommandHandler(ICommandHandler[CreateStaffMemberCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        staff_member_repository: IStaffMemberRepository,
        staff_password_hasher: IStaffPasswordHasher,
        principal_repository: IPrincipalRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._staff_member_repository = staff_member_repository
        self._staff_password_hasher = staff_password_hasher
        self._principal_repository = principal_repository

    async def handle(self, command: CreateStaffMemberCommand) -> None:
        email = StaffMemberEmailVO(command.email)
        password = StaffMemberPasswordVO(command.password)

        existing_member = await self._staff_member_repository.get_by_email(email)
        if existing_member is not None:
            raise StaffMemberWithGivenEmailAlreadyExists(email=email)

        principal = Principal.create(type=PrincipalTypeEnum.STAFF)

        member = StaffMember.create(
            id=principal.id,
            name=command.name,
            email=email,
            role=command.role,
            password_hash=self._staff_password_hasher.hash(password.value),
        )

        await self._principal_repository.save(principal)
        await self._staff_member_repository.save(member)
