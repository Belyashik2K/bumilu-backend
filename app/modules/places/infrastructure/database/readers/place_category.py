from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
)

from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.application.queries.categories.shared.views import (
    PlaceCategoriesPage,
    PlaceCategoryView,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceCategoryTranslationModel,
)


class SQLAlchemyPlaceCategoryReader(IPlaceCategoryReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def to_view(
        category: PlaceCategoryModel,
    ) -> PlaceCategoryView:
        return PlaceCategoryView(
            id=category.id,
            slug=category.slug,
            icon_key=category.icon_key,
            marker_color=category.marker_color,
            name=category.translations[0].name,
        )

    async def list(
        self,
        limit: int,
        offset: int,
        translation_language: LanguageEnum,
    ) -> PlaceCategoriesPage:
        count_stmt = (
            select(func.count(func.distinct(PlaceCategoryModel.id)))
            .select_from(PlaceCategoryModel)
            .join(PlaceCategoryModel.translations)
            .where(PlaceCategoryTranslationModel.language_code == translation_language)
        )

        items_stmt = (
            select(PlaceCategoryModel)
            .join(PlaceCategoryModel.translations)
            .where(PlaceCategoryTranslationModel.language_code == translation_language)
            .options(contains_eager(PlaceCategoryModel.translations))
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
            return PlaceCategoriesPage(
                items=[],
                total=total or 0,
            )

        categories: list[PlaceCategoryModel] = [row.PlaceCategoryModel for row in rows]
        total = rows[0].total_count

        return PlaceCategoriesPage(
            items=[self.to_view(category) for category in categories],
            total=total,
        )
