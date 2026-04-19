from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.staff.application.interfaces.readers.staff_member import (
    IStaffMemberReader,
)
from app.modules.staff.application.interfaces.repositories.staff_member import (
    IStaffMemberRepository,
)
from app.modules.staff.application.queries.get.handler import GetStaffMemberQueryHandler
from app.modules.staff.application.queries.get_all.handler import (
    GetStaffMembersListQueryHandler,
)


class StaffQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_staff_member_handler(
        self,
        staff_member_reader: IStaffMemberReader,
    ) -> GetStaffMemberQueryHandler:
        return GetStaffMemberQueryHandler(
            staff_member_reader=staff_member_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_staff_members_list_handler(
        self,
        staff_member_reader: IStaffMemberReader,
        staff_member_repository: IStaffMemberRepository,
    ) -> GetStaffMembersListQueryHandler:
        return GetStaffMembersListQueryHandler(
            staff_member_reader=staff_member_reader,
            staff_member_repository=staff_member_repository,
        )
