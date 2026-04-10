from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
)

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.mappers import (
    PlaceCategoryMapper,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
    PlaceCategoryReadModel,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceCategoryTranslationModel,
)
from app.modules.places.shared.enums.place_category_status import (
    PlaceCategoryStatusEnum,
)


class SQLAlchemyPlaceCategoryReader(IPlaceCategoryReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists(self, slug: str) -> bool:
        stmt = (
            select(func.count())
            .select_from(PlaceCategoryModel)
            .where(PlaceCategoryModel.slug == slug)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one() > 0

    async def get_by_id(
        self,
        category_id: UUID,
    ) -> PlaceCategoryReadModel | None:
        stmt = select(PlaceCategoryModel).where(PlaceCategoryModel.id == category_id)
        result = await self._session.execute(stmt)
        category = result.scalar_one_or_none()
        if category is None:
            return None
        return PlaceCategoryMapper.map_category(category)

    async def list(
        self,
        limit: int,
        offset: int,
        translation_language: LanguageEnum,
        status: PlaceCategoryStatusEnum | None = None,
    ) -> PageReadModel[LocalizedPlaceCategoryReadModel]:
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

        if status is not None:
            count_stmt = count_stmt.where(PlaceCategoryModel.status == status)
            items_stmt = items_stmt.where(PlaceCategoryModel.status == status)

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

        categories: list[PlaceCategoryModel] = [row.PlaceCategoryModel for row in rows]
        total = rows[0].total_count

        return PageReadModel(
            items=[
                PlaceCategoryMapper.map_localized_category(category)
                for category in categories
            ],
            total=total,
        )
