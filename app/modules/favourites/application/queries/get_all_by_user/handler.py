from app.core.application.queries import IQueryHandler
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.application.queries.get_all_by_user.query import (
    GetAllFavouritesByUserQuery,
    GetAllFavouritesByUserQueryResult,
)
from app.modules.favourites.application.shared.dtos import FavouriteItemDTO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.use_cases.get.exceptions import UserNotFound


class GetAllFavouritesByUserQueryHandler(
    IQueryHandler[
        GetAllFavouritesByUserQuery,
        GetAllFavouritesByUserQueryResult,
    ]
):
    def __init__(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
    ) -> None:
        self._favourite_repository = favourite_repository
        self._user_repository = user_repository

    async def handle(
        self, query: GetAllFavouritesByUserQuery
    ) -> GetAllFavouritesByUserQueryResult:
        user_id = UserIdVO.from_uuid(query.user_id)

        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        favourites = await self._favourite_repository.get_all_by_user_id(
            user_id=user_id,
        )

        return GetAllFavouritesByUserQueryResult(
            user_id=user_id.value,
            items=[
                FavouriteItemDTO(
                    entity_id=favourite.entity_id.value,
                    entity_type=favourite.entity_type,
                )
                for favourite in favourites
            ],
        )
