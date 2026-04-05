from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.value_objects.id import PlaceCategoryIdVO
from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.infrastructure.database.exception_catcher import (
    sqlalchemy_exception_catcher,
)
from app.modules.places.application.interfaces.repositories.place_category import (
    IPlaceCategoryRepository,
)
from app.modules.places.domain.categories.models.category.model import PlaceCategory
from app.modules.places.domain.categories.value_objects.icon_key import (
    PlaceCategoryIconKeyVO,
)
from app.modules.places.domain.categories.value_objects.marker_color.object import (
    PlaceCategoryMarkerColorVO,
)
from app.modules.places.domain.categories.value_objects.slug import PlaceCategorySlugVO
from app.modules.places.infrastructure.database.models import PlaceCategoryModel


class SQLAlchemyPlaceCategoryRepository(
    IPlaceCategoryRepository,
    SQLAlchemyBaseRepository[PlaceCategory, PlaceCategoryModel],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session=session,
            model_class=PlaceCategoryModel,
        )

    @sqlalchemy_exception_catcher
    async def save(self, entity: PlaceCategory) -> PlaceCategory:
        data = self._to_data(entity)
        merged_data = await self.session.merge(data)
        await self.session.flush()

        stmt = select(PlaceCategoryModel).where(PlaceCategoryModel.id == merged_data.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        return self._to_entity(model)

    def _to_data(self, entity: PlaceCategory) -> PlaceCategoryModel:
        return PlaceCategoryModel(
            id=entity.id.value,
            slug=entity.slug.value,
            icon_key=entity.icon_key.value,
            marker_color=entity.marker_color.value,
        )

    def _to_entity(self, model: PlaceCategoryModel) -> PlaceCategory:
        return PlaceCategory(
            id=PlaceCategoryIdVO.from_uuid(model.id),
            slug=PlaceCategorySlugVO(model.slug),
            icon_key=PlaceCategoryIconKeyVO(model.icon_key),
            marker_color=PlaceCategoryMarkerColorVO(model.marker_color),
            translation_language_codes=set(model.translation_language_codes or []),
        )
