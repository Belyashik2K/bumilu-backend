from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.staff.application.queries.shared.readers.staff_member import (
    IStaffMemberReader,
)
from app.modules.staff.application.queries.shared.views import StaffMemberInfoView
from app.modules.staff.infrastructure.database.models import StaffMemberModel


class SQLAlchemyStaffMemberReader(IStaffMemberReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, staff_member_id: UUID) -> StaffMemberInfoView | None:
        stmt = select(StaffMemberModel).where(StaffMemberModel.id == staff_member_id)
        result = await self._session.execute(stmt)
        data = result.scalar_one_or_none()
        if not data:
            return None
        return StaffMemberInfoView(
            id=data.id,
            email=data.email,
            role=data.role,
        )
