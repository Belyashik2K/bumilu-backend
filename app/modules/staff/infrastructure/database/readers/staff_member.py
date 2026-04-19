from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.queries.pagination import PageReadModel
from app.modules.staff.application.interfaces.readers.staff_member import (
    IStaffMemberReader,
)
from app.modules.staff.application.queries.shared.models.staff_member_info import (
    StaffMemberFullInfoReadModel,
    StaffMemberInfoReadModel,
)
from app.modules.staff.infrastructure.database.models import StaffMemberModel


class SQLAlchemyStaffMemberReader(IStaffMemberReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, staff_member_id: UUID) -> StaffMemberInfoReadModel | None:
        stmt = select(StaffMemberModel).where(StaffMemberModel.id == staff_member_id)
        result = await self._session.execute(stmt)
        data = result.scalar_one_or_none()
        if not data:
            return None
        return StaffMemberInfoReadModel(
            id=data.id,
            email=data.email,
            role=data.role,
        )

    async def get_full_info_by_id(
        self, staff_member_id: UUID
    ) -> StaffMemberFullInfoReadModel | None:
        stmt = select(StaffMemberModel).where(StaffMemberModel.id == staff_member_id)
        result = await self._session.execute(stmt)
        data = result.scalar_one_or_none()
        if not data:
            return None
        return StaffMemberFullInfoReadModel(
            id=data.id,
            email=data.email,
            role=data.role,
            name=data.name,
            created_at=data.created_at,
        )

    async def get_all(
        self,
        limit: int,
        offset: int,
    ) -> PageReadModel[StaffMemberFullInfoReadModel]:
        count_stmt = select(func.count(func.distinct(StaffMemberModel.id))).select_from(
            StaffMemberModel
        )

        items_stmt = select(StaffMemberModel)

        stmt = (
            items_stmt.add_columns(count_stmt.scalar_subquery().label("total_count"))
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        if not rows:
            total = await self._session.scalar(count_stmt)
            return PageReadModel(
                items=[],
                total=total or 0,
            )

        total = rows[0].total_count or 0
        items: list[StaffMemberFullInfoReadModel] = []

        for row in rows:
            data = row[0]
            items.append(
                StaffMemberFullInfoReadModel(
                    id=data.id,
                    email=data.email,
                    role=data.role,
                    name=data.name,
                    created_at=data.created_at,
                )
            )

        return PageReadModel(
            items=items,
            total=total,
        )
