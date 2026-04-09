from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.modules.places.application.commands.categories.update.command import (
    UpdatePlaceCategoryCommand,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.domain.categories.value_objects.icon_key import (
    PlaceCategoryIconKeyVO,
)
from app.modules.places.domain.categories.value_objects.marker_color.object import (
    PlaceCategoryMarkerColorVO,
)
from app.modules.places.domain.categories.value_objects.slug import PlaceCategorySlugVO


class UpdatePlaceCategoryCommandHandler(ICommandHandler[UpdatePlaceCategoryCommand]):
    def __init__(
        self,
        place_category_repository: IPlaceCategoryRepository,
        place_category_reader: IPlaceCategoryReader,
        transaction_manager: ITransactionManager,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_category_repository = place_category_repository
        self._place_category_reader = place_category_reader

    async def handle(self, command: UpdatePlaceCategoryCommand) -> None:
        category_id = PlaceCategoryIdVO.from_uuid(command.category_id)

        category = await self._place_category_repository.get_by_id(category_id)
        if category is None:
            raise ValueError(f"Place category with id {category_id} not found")

        new_slug = (
            PlaceCategorySlugVO(command.slug) if command.slug is not None else None
        )
        if new_slug is not None:
            category_with_slug = await self._place_category_repository.get_by_slug(
                new_slug
            )
            if category_with_slug and category_with_slug.id != category_id:
                raise ValueError(f"Place category with slug {new_slug} already exists")

        new_icon_key = (
            PlaceCategoryIconKeyVO(command.icon_key)
            if command.icon_key is not None
            else None
        )
        new_marker_color = (
            PlaceCategoryMarkerColorVO(command.marker_color)
            if command.marker_color is not None
            else None
        )

        category.update(
            slug=new_slug,
            icon_key=new_icon_key,
            marker_color=new_marker_color,
        )
        await self._place_category_repository.save(category)

        return None
