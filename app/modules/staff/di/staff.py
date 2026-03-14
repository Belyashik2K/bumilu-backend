from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.staff.application.interfaces.repositories.staff_member import (
    IStaffMemberRepository,
)
from app.modules.staff.application.queries.get.handler import GetStaffMemberQueryHandler
from app.modules.staff.application.queries.shared.readers.staff_member import (
    IStaffMemberReader,
)
from app.modules.staff.infrastructure.database.readers.staff_member import (
    SQLAlchemyStaffMemberReader,
)
from app.modules.staff.infrastructure.database.repositories.staff_member import (
    SQLAlchemyStaffMemberRepository,
)


class StaffProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IStaffMemberRepository)
    async def staff_member_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyStaffMemberRepository:
        return SQLAlchemyStaffMemberRepository(session=session)

    @provide(scope=Scope.REQUEST, provides=IStaffMemberReader)
    async def staff_member_reader(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyStaffMemberReader:
        return SQLAlchemyStaffMemberReader(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_staff_member_handler(
        self,
        staff_member_reader: IStaffMemberReader,
    ) -> GetStaffMemberQueryHandler:
        return GetStaffMemberQueryHandler(
            staff_member_reader=staff_member_reader,
        )
