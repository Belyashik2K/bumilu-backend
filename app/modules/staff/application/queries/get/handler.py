from app.core.application.queries import IQueryHandler
from app.modules.staff.application.queries.get.query import GetStaffMemberQuery
from app.modules.staff.application.queries.shared.exceptions import StaffMemberNotFound
from app.modules.staff.application.queries.shared.readers.staff_member import (
    IStaffMemberReader,
)
from app.modules.staff.application.queries.shared.views import StaffMemberInfoView


class GetStaffMemberQueryHandler(
    IQueryHandler[GetStaffMemberQuery, StaffMemberInfoView]
):
    def __init__(
        self,
        staff_member_reader: IStaffMemberReader,
    ) -> None:
        self.staff_member_reader = staff_member_reader

    async def handle(self, query: GetStaffMemberQuery) -> StaffMemberInfoView:
        staff_member = await self.staff_member_reader.get_by_id(query.staff_member_id)
        if not staff_member:
            raise StaffMemberNotFound(query.staff_member_id)  # type: ignore
        return staff_member
