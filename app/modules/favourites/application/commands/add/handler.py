from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.modules.favourites.application.commands.add import AddToFavouritesCommand
from app.modules.favourites.application.interfaces.entity_resolver import (
    IFavouriteEntityResolver,
)
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.application.shared.exceptions import (
    FavouriteEntityNotFound,
)
from app.modules.favourites.domain.models.favourite import Favourite
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.get.exceptions import UserNotFound


class AddToFavouritesCommandHandler(ICommandHandler[AddToFavouritesCommand]):
    def __init__(
        self,
        favourite_repository: IFavouriteRepository,
        user_repository: IUserRepository,
        entity_resolver: IFavouriteEntityResolver,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._favourite_repository = favourite_repository
        self._user_repository = user_repository
        self._entity_resolver = entity_resolver

    async def handle(self, command: AddToFavouritesCommand) -> None:
        entity_id = IdVO.from_uuid(command.entity_id)
        user_id = UserIdVO.from_uuid(command.user_id)

        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        favourite_entity = await self._entity_resolver.resolve(
            entity_type=command.entity_type,
            entity_id=entity_id,
        )
        if not favourite_entity:
            raise FavouriteEntityNotFound(
                entity_type=command.entity_type,
                entity_id=entity_id,
            )

        favourite = Favourite.create(
            user_id=user_id,
            entity_type=command.entity_type,
            entity_id=entity_id,
        )
        await self._favourite_repository.add_if_not_exists(favourite)

        return None
