from app.core.application.queries import IQueryHandler
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.get import (
    GetUserQuery,
    GetUserQueryResult,
)
from app.modules.users.application.queries.get.exceptions import UserNotFound


class GetUserQueryHandler(
    IQueryHandler[
        GetUserQuery,
        GetUserQueryResult,
    ]
):
    def __init__(
        self,
        user_repository: IUserRepository,
    ) -> None:
        self._user_repository = user_repository

    async def handle(
        self,
        query: GetUserQuery,
    ) -> GetUserQueryResult:
        user_id = UserIdVO.from_uuid(query.id)

        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        return GetUserQueryResult(
            id=str(user.id),
            email=str(user.email) if user.email else None,
            role=user.role,
        )
