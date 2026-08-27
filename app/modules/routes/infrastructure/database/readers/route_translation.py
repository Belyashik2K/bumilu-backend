from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.routes.application.interfaces.readers.route_translation import (
    IRouteTranslationReader,
)
from app.modules.routes.application.queries.shared.models.route_translation import (
    RouteTranslationReadModel,
)
from app.modules.routes.infrastructure.database.models import RouteTranslationModel


class SQLAlchemyRouteTranslationReader(IRouteTranslationReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_route_id_and_language_code(
        self,
        route_id: UUID,
        language_code: LanguageEnum,
    ) -> RouteTranslationReadModel | None:
        stmt = select(RouteTranslationModel).where(
            RouteTranslationModel.route_id == route_id,
            RouteTranslationModel.language_code == language_code,
        )
        result = await self._session.execute(stmt)
        translation = result.scalar_one_or_none()
        if translation is None:
            return None
        return RouteTranslationReadModel(
            language_code=translation.language_code,
            title=translation.title,
            description=translation.description,
            short_description=translation.short_description,
        )

    async def list_by_route_id(
        self,
        route_id: UUID,
        limit: int,
        offset: int,
    ) -> PageReadModel[RouteTranslationReadModel]:
        # TODO: Refactor to use query builder and avoid subquery for total count
        count_stmt = (
            select(func.count(func.distinct(RouteTranslationModel.id)))
            .select_from(RouteTranslationModel)
            .where(RouteTranslationModel.route_id == route_id)
        )

        items_stmt = select(RouteTranslationModel).where(
            RouteTranslationModel.route_id == route_id,
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
            total = await self._session.scalar(count_stmt) or 0
            return PageReadModel(total=total)

        translations: list[RouteTranslationModel] = [
            row.RouteTranslationModel for row in rows
        ]
        total = rows[0].total_count

        return PageReadModel(
            items=[
                RouteTranslationReadModel(
                    language_code=translation.language_code,
                    title=translation.title,
                    description=translation.description,
                    short_description=translation.short_description,
                )
                for translation in translations
            ],
            total=total,
        )
