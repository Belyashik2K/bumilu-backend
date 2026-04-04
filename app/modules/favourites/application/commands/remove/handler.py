from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
)
from app.modules.favourites.application.commands.remove import (
    RemoveFromFavouritesCommand,
)
from app.modules.favourites.application.interfaces.writers.favourite import (
    IFavouriteWriter,
)


class RemoveFromFavouritesCommandHandler(ICommandHandler[RemoveFromFavouritesCommand]):
    def __init__(
        self,
        favourite_writer: IFavouriteWriter,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._favourite_writer = favourite_writer

    async def handle(self, command: RemoveFromFavouritesCommand) -> None:
        user_id = PrincipalIdVO.from_uuid(command.user_id)
        entity_id = IdVO.from_uuid(command.entity_id)

        await self._favourite_writer.remove_if_exists(
            user_id=user_id,
            entity_type=command.entity_type,
            entity_id=entity_id,
        )

        return None
