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

    @staticmethod
    def _apply_filters(
        stmt,
        *,
        translation_language: LanguageEnum | None = None,
        status: PlaceCategoryStatusEnum | None = None,
    ):
        if translation_language is not None:
            stmt = stmt.join(PlaceCategoryModel.translations).where(
                PlaceCategoryTranslationModel.language_code == translation_language
            )

        if status is not None:
            stmt = stmt.where(PlaceCategoryModel.status == status)

        return stmt

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

    async def list_localized(
        self,
        limit: int,
        offset: int,
        translation_language: LanguageEnum,
        status: PlaceCategoryStatusEnum | None = None,
    ) -> PageReadModel[LocalizedPlaceCategoryReadModel]:
        count_stmt = self._apply_filters(
            select(func.count(func.distinct(PlaceCategoryModel.id))).select_from(
                PlaceCategoryModel
            ),
            translation_language=translation_language,
            status=status,
        )

        items_stmt = self._apply_filters(
            select(PlaceCategoryModel),
            translation_language=translation_language,
            status=status,
        ).options(contains_eager(PlaceCategoryModel.translations))

        total = await self._session.scalar(count_stmt)

        stmt = items_stmt.limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        categories = result.unique().scalars().all()

        return PageReadModel(
            items=[
                PlaceCategoryMapper.map_localized_category(category)
                for category in categories
            ],
            total=total or 0,
        )

    async def list_plain(
        self,
        limit: int,
        offset: int,
        status: PlaceCategoryStatusEnum | None = None,
    ) -> PageReadModel[PlaceCategoryReadModel]:
        count_stmt = self._apply_filters(
            select(func.count(PlaceCategoryModel.id)).select_from(PlaceCategoryModel),
            status=status,
        )

        items_stmt = self._apply_filters(
            select(PlaceCategoryModel),
            status=status,
        )

        total = await self._session.scalar(count_stmt)

        stmt = items_stmt.limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        categories = result.scalars().all()

        return PageReadModel(
            items=[
                PlaceCategoryMapper.map_category(category) for category in categories
            ],
            total=total or 0,
        )
