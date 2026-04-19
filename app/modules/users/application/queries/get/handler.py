from app.core.application.queries import IQueryHandler
from app.modules.users.application.queries.get.exceptions import UserNotFound
from app.modules.users.application.queries.get.query import (
    GetUserQuery,
)
from app.modules.users.application.queries.shared.readers import IUserReader
from app.modules.users.application.queries.shared.views import UserInfoView


class GetUserQueryHandler(
    IQueryHandler[
        GetUserQuery,
        UserInfoView,
    ]
):
    def __init__(self, user_reader: IUserReader) -> None:
        self._user_reader = user_reader

    async def handle(
        self,
        query: GetUserQuery,
    ) -> UserInfoView:
        user = await self._user_reader.get_by_id(query.user_id)
        if not user:
            # TODO: remove type ignore after fixing the type of user_id in UserNotFound
            raise UserNotFound(user_id=query.user_id)  # type: ignore

        return user
