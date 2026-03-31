from geoalchemy2 import Geography
from sqlalchemy import (
    cast,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.core.enums import LanguageEnum
from app.modules.places.infrastructure.database.models import PlaceModel
from app.modules.places.shared.enums.route_sort import RouteSortByEnum
from app.modules.routes.application.queries.shared.readers.route import IRouteReader
from app.modules.routes.application.queries.shared.views import (
    RouteCardPage,
    RouteCardView,
)
from app.modules.routes.infrastructure.database.models import (
    RouteModel,
    RoutePointModel,
    RouteTranslationModel,
)


class SQLAlchemyRouteReader(IRouteReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def to_card_view(
        route: RouteModel, *, total_places: int, distance_meters: float | None = None
    ) -> RouteCardView:
        translation = route.translations[0]

        return RouteCardView(
            id=route.id,
            title=translation.title,
            short_description=translation.short_description,
            total_places=total_places,
            m_to_start_place=round(distance_meters)
            if distance_meters is not None
            else None,
        )

    async def get_all(
        self,
        *,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
        latitude: float | None = None,
        longitude: float | None = None,
        sort_by: RouteSortByEnum | None = None,
    ) -> (
        RouteCardPage
    ):  # TODO: refactor to use separate queries for different sort_by values
        base_filters = [
            RouteTranslationModel.language_code == translation_language,
        ]

        total_places_subquery = (
            select(func.count(RoutePointModel.id))
            .where(RoutePointModel.route_id == RouteModel.id)
            .correlate(RouteModel)
            .scalar_subquery()
        )

        items_stmt = (
            select(RouteModel)
            .join(RouteModel.translations)
            .where(*base_filters)
            .options(
                contains_eager(RouteModel.translations),
            )
            .add_columns(total_places_subquery.label("total_places"))
        )

        count_stmt = (
            select(func.count(func.distinct(RouteModel.id)))
            .select_from(RouteModel)
            .join(RouteModel.translations)
            .where(*base_filters)
        )

        distance_expr = None

        if latitude is not None and longitude is not None:
            user_point = cast(
                func.ST_SetSRID(
                    func.ST_MakePoint(longitude, latitude),
                    4326,
                ),
                Geography,
            )

            distance_expr = func.ST_Distance(
                PlaceModel.location,
                user_point,
            ).label("distance_meters")

            items_stmt = (
                items_stmt.outerjoin(
                    RoutePointModel,
                    (RoutePointModel.route_id == RouteModel.id)
                    & (RoutePointModel.point_index == 1),
                )
                .outerjoin(
                    PlaceModel,
                    PlaceModel.id == RoutePointModel.place_id,
                )
                .add_columns(distance_expr)
            )

        if sort_by == RouteSortByEnum.NEAREST:
            if distance_expr is None:
                raise ValueError(
                    "latitude and longitude are required for NEAREST sorting"
                )

            items_stmt = items_stmt.order_by(
                distance_expr.asc(),
                RouteModel.id.asc(),
            )

        elif sort_by == RouteSortByEnum.NEW:
            items_stmt = items_stmt.order_by(
                RouteModel.created_at.desc(),
                RouteModel.id.desc(),
            )

        else:
            items_stmt = items_stmt.order_by(RouteModel.id.asc())

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
            return RouteCardPage(
                items=[],
                total=total or 0,
            )

        total = rows[0].total_count or 0
        items: list[RouteCardView] = []

        for row in rows:
            if distance_expr is not None:
                route, total_places, distance_meters, _total_count = row
            else:
                route, total_places, _total_count = row
                distance_meters = None

            items.append(
                self.to_card_view(
                    route,
                    total_places=total_places,
                    distance_meters=distance_meters,
                )
            )

        return RouteCardPage(
            items=items,
            total=total,
        )
