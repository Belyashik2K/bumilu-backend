from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.interfaces.readers.place_translation import (
    IPlaceTranslationReader,
)
from app.modules.places.application.queries.places.shared.models.place_translation import (
    PlaceTranslationReadModel,
)
from app.modules.places.infrastructure.database.models import PlaceTranslationModel


class SQLAlchemyPlaceTranslationReader(IPlaceTranslationReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_place_id_and_language_code(
        self,
        place_id: UUID,
        language_code: LanguageEnum,
    ) -> PlaceTranslationReadModel | None:
        stmt = select(PlaceTranslationModel).where(
            PlaceTranslationModel.place_id == place_id,
            PlaceTranslationModel.language_code == language_code,
        )
        result = await self._session.execute(stmt)
        translation = result.scalar_one_or_none()
        if translation is None:
            return None
        return PlaceTranslationReadModel(
            language_code=translation.language_code,
            title=translation.title,
            description=translation.description,
            short_description=translation.short_description,
            display_address=translation.address_display,
        )

    async def list_by_place_id(
        self,
        place_id: UUID,
        limit: int,
        offset: int,
    ) -> PageReadModel[PlaceTranslationReadModel]:
        count_stmt = (
            select(func.count(func.distinct(PlaceTranslationModel.id)))
            .select_from(PlaceTranslationModel)
            .where(PlaceTranslationModel.place_id == place_id)
        )

        items_stmt = select(PlaceTranslationModel).where(
            PlaceTranslationModel.place_id == place_id,
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

        translations: list[PlaceTranslationModel] = [
            row.PlaceTranslationModel for row in rows
        ]
        total = rows[0].total_count

        return PageReadModel(
            items=[
                PlaceTranslationReadModel(
                    language_code=translation.language_code,
                    title=translation.title,
                    description=translation.description,
                    short_description=translation.short_description,
                    display_address=translation.address_display,
                )
                for translation in translations
            ],
            total=total,
        )
