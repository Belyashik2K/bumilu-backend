from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.queries.pagination import PageReadModel
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
        limit: int,
        offset: int,
    ) -> PageReadModel[PlaceCategoryTranslationReadModel]:
        count_stmt = (
            select(func.count(func.distinct(PlaceCategoryTranslationModel.id)))
            .select_from(PlaceCategoryTranslationModel)
            .where(PlaceCategoryTranslationModel.category_id == category_id)
        )

        items_stmt = select(PlaceCategoryTranslationModel).where(
            PlaceCategoryTranslationModel.category_id == category_id,
        )

        total_subquery = count_stmt.scalar_subquery()

        stmt = (
            items_stmt.add_columns(total_subquery.label("total_count"))
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        if not rows:
            total = await self._session.scalar(count_stmt)
            return PageReadModel(total=total)

        translations: list[PlaceCategoryTranslationModel] = [
            row.PlaceCategoryTranslationModel for row in rows
        ]
        total = rows[0].total_count

        return PageReadModel(
            items=[
                PlaceCategoryTranslationReadModel(
                    language_code=translation.language_code,
                    name=translation.name,
                )
                for translation in translations
            ],
            total=total,
        )
