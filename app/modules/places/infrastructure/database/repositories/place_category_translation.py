from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceCategoryTranslationIdVO,
)
from app.core.enums import LanguageEnum
from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.modules.places.application.interfaces.repositories.place_category_translation import (
    IPlaceCategoryTranslationRepository,
)
from app.modules.places.domain.categories.models.category_translation.model import (
    PlaceCategoryTranslation,
)
from app.modules.places.domain.categories.value_objects.name.object import (
    PlaceCategoryNameVO,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryTranslationModel,
)


class SQLAlchemyPlaceCategoryTranslationRepository(
    IPlaceCategoryTranslationRepository,
    SQLAlchemyBaseRepository[PlaceCategoryTranslation, PlaceCategoryTranslationModel],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session=session,
            model_class=PlaceCategoryTranslationModel,
        )

    def _to_data(
        self, entity: PlaceCategoryTranslation
    ) -> PlaceCategoryTranslationModel:
        return PlaceCategoryTranslationModel(
            id=entity.id.value,
            category_id=entity.category_id.value,
            language_code=entity.language_code,
            name=entity.name.value,
        )

    def _to_entity(
        self, model: PlaceCategoryTranslationModel
    ) -> PlaceCategoryTranslation:
        return PlaceCategoryTranslation(
            id=PlaceCategoryTranslationIdVO.from_uuid(model.id),
            category_id=PlaceCategoryIdVO.from_uuid(model.category_id),
            language_code=model.language_code,
            name=PlaceCategoryNameVO(model.name),
        )

    async def get_by_category_id_and_language_code(
        self, category_id: PlaceCategoryIdVO, language_code: LanguageEnum
    ) -> PlaceCategoryTranslation | None:
        stmt = select(PlaceCategoryTranslationModel).where(
            PlaceCategoryTranslationModel.category_id == category_id.value,
            PlaceCategoryTranslationModel.language_code == language_code,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    # TODO: catchers
    async def delete_by_id(self, translation_id: PlaceCategoryTranslationIdVO) -> None:
        stmt = delete(PlaceCategoryTranslationModel).where(
            PlaceCategoryTranslationModel.id == translation_id.value,
        )
        await self.session.execute(stmt)
        await self.session.flush()
