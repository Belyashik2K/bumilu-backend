from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.application.commands.categories.change_status.query import (
    ChangePlaceCategoryStatusCommand,
)
from app.modules.places.application.exceptions.place_category import (
    PlaceCategoryNotFound,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)


class ChangePlaceCategoryStatusCommandHandler(
    ICommandHandler[ChangePlaceCategoryStatusCommand]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_category_repository: IPlaceCategoryRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_category_repository = place_category_repository

    async def handle(self, command: ChangePlaceCategoryStatusCommand) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)

        category = await self._place_category_repository.get_by_id(category_id)
        if category is None:
            raise PlaceCategoryNotFound(category_id=category_id.value)

        category.change_status(command.status)
        await self._place_category_repository.save(category)
