from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.shared.domain.value_objects.id import PrincipalIdVO
from app.modules.staff.application.repositories.staff_member import (
    IStaffMemberRepository,
)
from app.modules.staff.domain.models.staff_member import StaffMember
from app.modules.staff.domain.value_objects.staff_email import StaffEmailVO
from app.modules.staff.infrastructure.database.models import StaffMemberModel


class SQLAlchemyStaffMemberRepository(
    IStaffMemberRepository,
    SQLAlchemyBaseRepository[StaffMember, StaffMemberModel],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_class=StaffMemberModel)  # type: ignore

    def _to_data(self, entity: StaffMember) -> StaffMemberModel:
        return StaffMemberModel(
            id=entity.id.value,
            name=entity.name,
            email=entity.email.value,
            password_hash=entity.password_hash,
            role=entity.role,
        )

    def _to_entity(self, data: StaffMemberModel) -> StaffMember:
        return StaffMember(
            id=PrincipalIdVO.from_uuid(data.id),
            name=data.name,
            email=StaffEmailVO.from_string(data.email),
            password_hash=data.password_hash,
            role=data.role,
        )

    async def get_by_email(self, email: StaffEmailVO) -> StaffMember | None:
        stmt = select(StaffMemberModel).where(StaffMemberModel.email == email.value)
        result = await self.session.execute(stmt)
        data = result.scalar_one_or_none()
        if data is None:
            return None
        return self._to_entity(data)

    async def total_staff_members(self) -> int:
        stmt = select(func.count(StaffMemberModel.id))
        result = await self.session.execute(stmt)
        total = result.scalar_one()
        return total
