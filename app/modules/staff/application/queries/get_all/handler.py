from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import PaginatedView
from app.core.domain.value_objects.id import PrincipalIdVO
from app.modules.staff.application.exceptions.staff_member import (
    ActorRoleNotAllowedToPerformAction,
)
from app.modules.staff.application.interfaces.readers.staff_member import (
    IStaffMemberReader,
)
from app.modules.staff.application.interfaces.repositories.staff_member import (
    IStaffMemberRepository,
)
from app.modules.staff.application.queries.get_all.query import GetStaffMembersListQuery
from app.modules.staff.application.queries.shared.models.staff_member_info import (
    StaffMemberFullInfoReadModel,
)
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum


class GetStaffMembersListQueryHandler(
    IQueryHandler[GetStaffMembersListQuery, PaginatedView[StaffMemberFullInfoReadModel]]
):
    def __init__(
        self,
        staff_member_reader: IStaffMemberReader,
        staff_member_repository: IStaffMemberRepository,
    ) -> None:
        self.staff_member_reader = staff_member_reader
        self.staff_member_repository = staff_member_repository

    async def handle(
        self, query: GetStaffMembersListQuery
    ) -> PaginatedView[StaffMemberFullInfoReadModel]:
        actor_id = PrincipalIdVO.from_uuid(query.actor_id)
        actor = await self.staff_member_repository.get_by_id(actor_id)

        # TODO: This check is repeated in multiple places, consider moving it to a decorator
        if actor is None or actor.role != StaffRoleEnum.OWNER:
            raise ActorRoleNotAllowedToPerformAction(
                actor_role=actor.role if actor is not None else None,
                action="Get staff members list",
            )

        data = await self.staff_member_reader.get_all(
            limit=query.limit,
            offset=query.offset,
        )
        return PaginatedView.create(
            items=data.items,
            total=data.total,
            limit=query.limit,
            offset=query.offset,
        )
