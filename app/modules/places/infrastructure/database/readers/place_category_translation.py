from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.models.place_category import (
    PlaceCategoryTranslationReadModel,
)
from app.modules.places.application.queries.categories.shared.readers.place_category_translation import (
    IPlaceCategoryTranslationReader,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryTranslationModel,
)


class SQLAlchemyPlaceCategoryTranslationReader(IPlaceCategoryTranslationReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_category_id_and_language_code(
        self,
        category_id: UUID,
        language_code: LanguageEnum,
    ) -> PlaceCategoryTranslationReadModel | None:
        stmt = select(PlaceCategoryTranslationModel).where(
            PlaceCategoryTranslationModel.category_id == category_id,
            PlaceCategoryTranslationModel.language_code == language_code,
        )
        result = await self._session.execute(stmt)
        translation = result.scalar_one_or_none()
        if translation is None:
            return None
        return PlaceCategoryTranslationReadModel(
            language_code=translation.language_code,
            name=translation.name,
        )

    async def list_by_category_id(
        self,
        category_id: UUID,
    ) -> list[PlaceCategoryTranslationReadModel]:
        stmt = select(PlaceCategoryTranslationModel).where(
            PlaceCategoryTranslationModel.category_id == category_id,
        )
        result = await self._session.execute(stmt)
        translations = result.scalars().all()
        return [
            PlaceCategoryTranslationReadModel(
                language_code=translation.language_code,
                name=translation.name,
            )
            for translation in translations
        ]  # TODO: move to mappers
