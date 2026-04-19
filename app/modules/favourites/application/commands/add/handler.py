from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
)
from app.modules.favourites.application.commands.add import AddToFavouritesCommand
from app.modules.favourites.application.interfaces.target_checker import (
    IFavouriteTargetChecker,
)
from app.modules.favourites.application.interfaces.writers.favourite import (
    IFavouriteWriter,
)
from app.modules.favourites.application.shared.exceptions import (
    FavouriteEntityNotFound,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.queries.get.exceptions import UserNotFound


class AddToFavouritesCommandHandler(ICommandHandler[AddToFavouritesCommand]):
    def __init__(
        self,
        favourite_writer: IFavouriteWriter,
        user_repository: IUserRepository,
        favourite_target_checker: IFavouriteTargetChecker,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._favourite_writer = favourite_writer
        self._user_repository = user_repository
        self._favourite_target_checker = favourite_target_checker

    async def handle(self, command: AddToFavouritesCommand) -> None:
        entity_id = IdVO.from_uuid(command.entity_id)
        user_id = PrincipalIdVO.from_uuid(command.user_id)

        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        exists = await self._favourite_target_checker.exists(
            entity_type=command.entity_type,
            entity_id=entity_id,
        )
        if not exists:
            raise FavouriteEntityNotFound(
                entity_type=command.entity_type,
                entity_id=entity_id,
            )

        await self._favourite_writer.add_if_not_exists(
            user_id=user_id,
            entity_type=command.entity_type,
            entity_id=entity_id,
        )

        return None
