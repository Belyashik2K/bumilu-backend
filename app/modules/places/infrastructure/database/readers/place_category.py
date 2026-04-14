from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.categories.shared.mappers import (
    PlaceCategoryMapper,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    AdminPlaceCategoryReadModel,
    LocalizedPlaceCategoryReadModel,
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

COMMON_SELECT = select(PlaceCategoryModel).order_by(PlaceCategoryModel.slug.asc())


class SQLAlchemyPlaceCategoryReader(IPlaceCategoryReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _apply_filters(
        stmt,
        *,
        translation_language: LanguageEnum | None = None,
        optional_translation_language: LanguageEnum | None = None,
        status: PlaceCategoryStatusEnum | None = None,
        with_translation_loader: bool = True,
    ):
        if translation_language is not None:
            stmt = stmt.join(PlaceCategoryModel.translations).where(
                PlaceCategoryTranslationModel.language_code == translation_language
            )
            if with_translation_loader:
                stmt = stmt.options(contains_eager(PlaceCategoryModel.translations))

        if optional_translation_language is not None:
            if translation_language is not None:
                raise ValueError(
                    "Only one of translation_language or optional_translation_language can be provided"
                )

            stmt = stmt.outerjoin(
                PlaceCategoryModel.translations.and_(
                    PlaceCategoryTranslationModel.language_code
                    == optional_translation_language
                )
            )
            if with_translation_loader:
                stmt = stmt.options(contains_eager(PlaceCategoryModel.translations))

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

    async def exists_by_id(self, category_id: UUID) -> bool:
        stmt = (
            select(func.count())
            .select_from(PlaceCategoryModel)
            .where(PlaceCategoryModel.id == category_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one() > 0

    async def get_admin_by_id(
        self,
        category_id: UUID,
        optional_translation_language: LanguageEnum,
    ) -> AdminPlaceCategoryReadModel | None:
        stmt = self._apply_filters(
            (select(PlaceCategoryModel).where(PlaceCategoryModel.id == category_id)),
            optional_translation_language=optional_translation_language,
        )

        result = await self._session.execute(stmt)
        category = result.unique().scalar_one_or_none()
        if category is None:
            return None
        return PlaceCategoryMapper.map_admin_category(
            category,
            translation=category.translations[0] if category.translations else None,
        )

    async def list_public_localized(
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
            with_translation_loader=False,
        )

        items_stmt = self._apply_filters(
            COMMON_SELECT,
            translation_language=translation_language,
            status=status,
            with_translation_loader=True,
        )

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

    async def list_admin(
        self,
        limit: int,
        offset: int,
        optional_translation_language: LanguageEnum,
        status: PlaceCategoryStatusEnum | None = None,
    ) -> PageReadModel[AdminPlaceCategoryReadModel]:
        count_stmt = self._apply_filters(
            select(func.count(PlaceCategoryModel.id)).select_from(PlaceCategoryModel),
            status=status,
        )

        items_stmt = self._apply_filters(
            COMMON_SELECT,
            status=status,
            optional_translation_language=optional_translation_language,
        )

        total = await self._session.scalar(count_stmt)

        stmt = items_stmt.limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        categories = result.unique().scalars().all()

        return PageReadModel(
            items=[
                PlaceCategoryMapper.map_admin_category(
                    category,
                    translation=category.translations[0]
                    if category.translations
                    else None,
                )
                for category in categories
            ],
            total=total or 0,
        )
