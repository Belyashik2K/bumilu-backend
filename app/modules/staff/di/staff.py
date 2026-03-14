from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.staff.application.repositories.staff_member import (
    IStaffMemberRepository,
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
