from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.modules.auth.application.interfaces.hashers import IStaffPasswordHasher
from app.modules.auth.application.interfaces.repositories.principal import (
    IPrincipalRepository,
)
from app.modules.staff.application.commands.create_member.handler import (
    CreateStaffMemberCommandHandler,
)
from app.modules.staff.application.interfaces.repositories.staff_member import (
    IStaffMemberRepository,
)


class StaffCommandHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def create_staff_member_handler(
        self,
        transaction_manager: ITransactionManager,
        staff_member_repository: IStaffMemberRepository,
        staff_password_hasher: IStaffPasswordHasher,
        principal_repository: IPrincipalRepository,
    ) -> CreateStaffMemberCommandHandler:
        return CreateStaffMemberCommandHandler(
            staff_member_repository=staff_member_repository,
            staff_password_hasher=staff_password_hasher,
            principal_repository=principal_repository,
            transaction_manager=transaction_manager,
        )
