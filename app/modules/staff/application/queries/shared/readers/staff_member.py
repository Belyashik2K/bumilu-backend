from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.modules.staff.application.queries.shared.views import StaffMemberInfoView


class IStaffMemberReader(ABC):
    @abstractmethod
    async def get_by_id(self, staff_member_id: UUID) -> StaffMemberInfoView | None: ...
