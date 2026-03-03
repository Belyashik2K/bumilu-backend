from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.application.use_cases.get_all_by_user import (
    GetAllFavouritesByUserInputDTO,
    GetAllFavouritesByUserOutputDTO,
)
from app.modules.favourites.application.use_cases.shared.dtos import FavouriteItemDTO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.use_cases.get.exceptions import UserNotFound


class GetAllFavouritesByUserUseCase(
    IBaseUseCase[
        GetAllFavouritesByUserInputDTO,
        GetAllFavouritesByUserOutputDTO,
    ]
):
    def __init__(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
    ) -> None:
        self._favourite_repository = favourite_repository
        self._user_repository = user_repository

    async def execute(
        self, input_data: GetAllFavouritesByUserInputDTO
    ) -> GetAllFavouritesByUserOutputDTO:
        user_id = UserIdVO.from_uuid(input_data.user_id)

        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        favourites = await self._favourite_repository.get_all_by_user_id(
            user_id=user_id,
        )

        return GetAllFavouritesByUserOutputDTO(
            items=[
                FavouriteItemDTO(
                    entity_id=favourite.entity_id.value,
                    entity_type=favourite.entity_type,
                )
                for favourite in favourites
            ],
        )
