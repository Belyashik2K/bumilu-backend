from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.constants import UnsetType
from app.core.domain.value_objects.id import (
    PlaceIdVO,
)
from app.core.domain.value_objects.location import LocationVO
from app.modules.places.application.commands.places.update.command import (
    UpdatePlaceCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
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
from app.modules.places.domain.places.value_objects.taxi_address.object import (
    PlaceTaxiAddressVO,
)


class UpdatePlaceCommandHandler(ICommandHandler[UpdatePlaceCommand]):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
        place_category_repository: IPlaceCategoryRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository
        self._place_category_repository = place_category_repository

    async def handle(self, command: UpdatePlaceCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id(place_id)
        if place is None:
            raise PlaceNotFound(place_id=place_id.value)

        if not isinstance(command.category_slug, UnsetType):
            category_slug = PlaceCategorySlugVO(command.category_slug)
            category = await self._place_category_repository.get_by_slug(category_slug)
            if category is None:
                raise PlaceCategorySlugNotFound(slug=category_slug.value)
            category_id = category.id
        else:
            category_id = place.category_id

        new_location = (
            LocationVO.from_coordinates(command.latitude, command.longitude)
            if not isinstance(command.latitude, UnsetType)
            and not isinstance(command.longitude, UnsetType)
            else place.location
        )
        new_address_taxi = (
            PlaceTaxiAddressVO(command.address_taxi)
            if not isinstance(command.address_taxi, UnsetType)
            else place.address_taxi
        )
        new_address_taxi_comment = (
            command.address_taxi_comment
            if not isinstance(command.address_taxi_comment, UnsetType)
            else place.address_taxi_comment
        )

        place.update(
            category_id=category_id,
            location=new_location,
            address_taxi=new_address_taxi,
            address_taxi_comment=new_address_taxi_comment,
        )
        await self._place_repository.save(place)
