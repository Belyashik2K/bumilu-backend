from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.modules.favourites.application.commands.remove import (
    RemoveFromFavouritesInputDTO,
    RemoveFromFavouritesOutputDTO,
)
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.domain.models.favourite import Favourite


class RemoveFromFavouritesUseCase(
    IBaseUseCase[RemoveFromFavouritesInputDTO, RemoveFromFavouritesOutputDTO]
):
    def __init__(self, favourite_repository: IFavouriteRepository) -> None:
        self._favourite_repository = favourite_repository

    async def execute(
        self, input_data: RemoveFromFavouritesInputDTO
    ) -> RemoveFromFavouritesOutputDTO:
        user_id = UserIdVO.from_uuid(input_data.user_id)
        entity_id = IdVO.from_uuid(input_data.entity_id)

        favourite = Favourite.create(
            user_id=user_id,
            entity_type=input_data.entity_type,
            entity_id=entity_id,
        )

        await self._favourite_repository.remove_if_exists(favourite=favourite)
        return RemoveFromFavouritesOutputDTO()
