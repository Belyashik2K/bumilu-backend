from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.modules.favourites.application.interfaces.entity_resolver import (
    IFavouriteEntityResolver,
)
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.application.use_cases.add import (
    AddToFavouritesInputDTO,
    AddToFavouritesOutputDTO,
)
from app.modules.favourites.domain.models.favourite import Favourite
from app.modules.reviews.application.use_cases.shared.exceptions import EntityNotFound
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.use_cases.get.exceptions import UserNotFound


class AddToFavouritesUseCase(
    IBaseUseCase[
        AddToFavouritesInputDTO,
        AddToFavouritesOutputDTO,
    ]
):
    def __init__(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
        entity_resolver: IFavouriteEntityResolver,
    ) -> None:
        self._favourite_repository = favourite_repository
        self._user_repository = user_repository
        self._entity_resolver = entity_resolver

    async def execute(
        self, input_data: AddToFavouritesInputDTO
    ) -> AddToFavouritesOutputDTO:
        entity_id = IdVO.from_uuid(input_data.entity_id)
        user_id = UserIdVO.from_uuid(input_data.user_id)

        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        favourite_entity = self._entity_resolver.resolve(
            entity_type=input_data.entity_type,
            entity_id=entity_id,
        )
        if not favourite_entity:
            raise EntityNotFound(
                entity_type=input_data.entity_type,  # type: ignore
                entity_id=entity_id,
            )

        favourite = Favourite.create(
            user_id=user_id,
            entity_type=input_data.entity_type,
            entity_id=entity_id,
        )
        await self._favourite_repository.add_if_not_exists(favourite)

        return AddToFavouritesOutputDTO()
