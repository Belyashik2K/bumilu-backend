from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from app.core.application.queries.pagination import PageReadModel
from app.modules.staff.application.queries.shared.models.staff_member_info import (
    StaffMemberFullInfoReadModel,
    StaffMemberInfoReadModel,
)


class IStaffMemberReader(ABC):
    @abstractmethod
    async def get_by_id(
        self, staff_member_id: UUID
    ) -> StaffMemberInfoReadModel | None: ...

    @abstractmethod
    async def get_full_info_by_id(
        self, staff_member_id: UUID
    ) -> StaffMemberFullInfoReadModel | None: ...

    @abstractmethod
    async def get_all(
        self,
        limit: int,
        offset: int,
    ) -> PageReadModel[StaffMemberFullInfoReadModel]: ...
