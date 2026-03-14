from abc import (
    ABC,
    abstractmethod,
)

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.staff.domain.models.staff_member import StaffMember
from app.modules.staff.domain.value_objects.staff_email import StaffEmailVO


class IStaffMemberRepository(IBaseRepository[StaffMember], ABC):
    @abstractmethod
    async def get_by_email(self, email: StaffEmailVO) -> StaffMember | None: ...
