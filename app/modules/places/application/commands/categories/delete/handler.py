from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.application.commands.categories.delete.command import (
    DeletePlaceCategoryCommand,
)
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)


class DeletePlaceCategoryCommandHandler(ICommandHandler[DeletePlaceCategoryCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_category_repository: IPlaceCategoryRepository,
        place_reader: IPlaceReader,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_category_repository = place_category_repository
        self._place_reader = place_reader

    async def handle(self, command: DeletePlaceCategoryCommand) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)
        category = await self._place_category_repository.get_by_id(category_id)
        if category is None:
            raise ValueError(f"Place category with id {category_id} not found")

        places_count = await self._place_reader.count_by_category_id(
            category_id.value
        )  # TODO: migrate to VO
        if places_count != 0:
            raise ValueError(
                f"Cannot delete place category with id {category_id} because there are {places_count} places assigned to it"
            )

        await self._place_category_repository.delete_by_id(category.id)
