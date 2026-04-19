from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
)
from app.modules.favourites.application.interfaces.repositories.place_favourite import (
    IPlaceFavouriteRepository,
)
from app.modules.favourites.application.interfaces.writers.favourite import (
    IFavouriteWriter,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class FavouriteWriter(IFavouriteWriter):
    def __init__(
        self,
        place_favourite_repository: IPlaceFavouriteRepository,
    ) -> None:
        self.mapped_repositories = {
            FavouriteEntityTypeEnum.PLACE: place_favourite_repository,
        }

    async def add_if_not_exists(
        self,
        user_id: PrincipalIdVO,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> None:
        repository = self.mapped_repositories.get(entity_type)
        if not repository:
            raise ValueError(f"No repository found for entity type {entity_type}")

        await repository.add_if_not_exists(
            user_id=user_id,
            entity_id=entity_id,
        )

    async def remove_if_exists(
        self,
        user_id: PrincipalIdVO,
        entity_type: FavouriteEntityTypeEnum,
        entity_id: IdVO,
    ) -> None:
        repository = self.mapped_repositories.get(entity_type)
        if not repository:
            raise ValueError(
                f"No repository found for entity type {entity_type}"
            )  # TODO: custom exception

        await repository.remove_if_exists(
            user_id=user_id,
            entity_id=entity_id,
        )
