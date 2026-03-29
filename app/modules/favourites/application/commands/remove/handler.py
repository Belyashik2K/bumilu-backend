from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
)
from app.modules.favourites.application.commands.remove import (
    RemoveFromFavouritesCommand,
)
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.domain.models.favourite import Favourite


class RemoveFromFavouritesCommandHandler(ICommandHandler[RemoveFromFavouritesCommand]):
    def __init__(
        self,
        favourite_repository: IFavouriteRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._favourite_repository = favourite_repository

    async def handle(self, command: RemoveFromFavouritesCommand) -> None:
        user_id = PrincipalIdVO.from_uuid(command.user_id)
        entity_id = IdVO.from_uuid(command.entity_id)

        favourite = Favourite.create(
            user_id=user_id,
            entity_type=command.entity_type,
            entity_id=entity_id,
        )

        await self._favourite_repository.remove_if_exists(favourite=favourite)
        return None
