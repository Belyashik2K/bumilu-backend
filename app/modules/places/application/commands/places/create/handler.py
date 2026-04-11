from app.core.application.commands import ICommandHandlerWithResult
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.location import LocationVO
from app.modules.places.application.commands.places.create.command import (
    CreatePlaceCommand,
    CreatePlaceCommandResult,
)
from app.modules.places.application.exceptions.place_category import (
    PlaceCategorySlugNotFound,
)
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.domain.categories.value_objects.slug import PlaceCategorySlugVO
from app.modules.places.domain.places.models.place.model import Place
from app.modules.places.domain.places.value_objects.taxi_address.object import (
    TaxiAddressVO,
)


class CreatePlaceCommandHandler(
    ICommandHandlerWithResult[CreatePlaceCommand, CreatePlaceCommandResult]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_category_repository: IPlaceCategoryRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository
        self._place_category_repository = place_category_repository

    async def handle(self, command: CreatePlaceCommand) -> CreatePlaceCommandResult:
        category_slug = PlaceCategorySlugVO(command.category_slug)
        category = await self._place_category_repository.get_by_slug(category_slug)
        if category is None:
            raise PlaceCategorySlugNotFound(slug=category_slug.value)

        place = Place.create(
            category_id=category.id,
            location=LocationVO(latitude=command.latitude, longitude=command.longitude),
            address_taxi=TaxiAddressVO(command.address_taxi),
            address_taxi_comment=command.address_taxi_comment,
        )
        await self._place_repository.save(place)

        return CreatePlaceCommandResult(id=place.id.value)
