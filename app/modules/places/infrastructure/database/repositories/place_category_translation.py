from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceCategoryTranslationIdVO,
)
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
