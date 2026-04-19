from uuid import UUID

from geoalchemy2 import Geography
from sqlalchemy import (
    cast,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    selectinload,
    with_loader_criteria,
)

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.places.application.queries.places.shared.mappers import (
    PlaceReadModelMapper,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceCategoryTranslationModel,
    PlaceModel,
    PlaceTranslationModel,
    PlaceWorkingDayModel,
)
from app.modules.places.shared.enums.route_sort import RouteSortByEnum
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.queries.shared.models.route_card import (
    RouteCardReadModel,
)
from app.modules.routes.application.queries.shared.models.route_details import (
    RouteDetailsReadModel,
)
from app.modules.routes.application.queries.shared.models.route_point import (
    RoutePointReadModel,
    RouteWaypointModel,
)
from app.modules.routes.infrastructure.database.models import (
    RouteModel,
    RoutePointModel,
    RouteTranslationModel,
)
from app.modules.routes.shared.enums.route_status import RouteStatusEnum


class SQLAlchemyRouteReader(IRouteReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
        self,
        route_id: UUID,
        *,
        translation_language: LanguageEnum,
    ) -> RouteDetailsReadModel | None:
        place_loader = selectinload(RouteModel.points).joinedload(RoutePointModel.place)

        stmt = (
            select(RouteModel)
            .join(RouteModel.translations)
            .where(
                RouteModel.id == route_id,
                RouteModel.status == RouteStatusEnum.PUBLISHED,
                RouteTranslationModel.language_code == translation_language,
            )
            .options(
                contains_eager(RouteModel.translations),
                place_loader.selectinload(PlaceModel.translations),
                place_loader.selectinload(PlaceModel.photos),
                place_loader.joinedload(PlaceModel.category).selectinload(
                    PlaceCategoryModel.translations
                ),
                place_loader.selectinload(PlaceModel.working_days).selectinload(
                    PlaceWorkingDayModel.working_hours
                ),
                with_loader_criteria(
                    PlaceTranslationModel,
                    PlaceTranslationModel.language_code == translation_language,
                    include_aliases=True,
                ),
                with_loader_criteria(
                    PlaceCategoryTranslationModel,
                    PlaceCategoryTranslationModel.language_code == translation_language,
                    include_aliases=True,
                ),
            )
        )

        result = await self._session.execute(stmt)
        route = result.unique().scalar_one_or_none()
        if route is None:
            return None

        return RouteDetailsReadModel(
            id=route.id,
            title=route.translations[0].title,
            description=route.translations[0].description,
            short_description=route.translations[0].short_description,
            points=[
                RoutePointReadModel(
                    index=point.point_index,
                    preview=PlaceReadModelMapper.map_card(
                        place=point.place,
                        rating_average=point.place.rating_average,
                        reviews_count=point.place.rating_reviews_count,
                    ),
                )
                for point in route.points
            ],
            total_points=len(route.points),
        )

    async def count_by_place_id(self, place_id: UUID) -> int:
        stmt = select(func.count(RoutePointModel.id)).where(
            RoutePointModel.place_id == place_id
        )

        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def get_route_waypoints(
        self,
        route_id: UUID,
    ) -> list[RouteWaypointModel]:
        stmt = (
            select(RoutePointModel)
            .join(RoutePointModel.route)
            .where(
                RouteModel.status == RouteStatusEnum.PUBLISHED,
                RoutePointModel.route_id == route_id,
            )
            .options(
                joinedload(
                    RoutePointModel.place,
                ),
            )
            .order_by(RoutePointModel.point_index.asc())
        )

        result = await self._session.execute(stmt)
        points = result.scalars().all()

        return [
            RouteWaypointModel(
                index=point.point_index,
                latitude=point.place.latitude,
                longitude=point.place.longitude,
            )
            for point in points
        ]

    async def get_admin_route_points(
        self,
        route_id: UUID,
        optional_translation_language: LanguageEnum,
    ) -> list[RoutePointReadModel]: ...

    async def get_all(
        self,
        *,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
        latitude: float | None = None,
        longitude: float | None = None,
        sort_by: RouteSortByEnum | None = None,
    ) -> PageReadModel[RouteCardReadModel]:
        # TODO: refactor to use separate queries for different sort_by values
        base_filters = [
            RouteModel.status == RouteStatusEnum.PUBLISHED,
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
            return PageReadModel(
                items=[],
                total=total or 0,
            )

        total = rows[0].total_count or 0
        items: list[RouteCardReadModel] = []

        for row in rows:
            if distance_expr is not None:
                route, total_places, distance_meters, _total_count = row
            else:
                route, total_places, _total_count = row
                distance_meters = None

            items.append(
                RouteCardReadModel(
                    id=route.id,
                    title=route.translations[0].title,
                    short_description=route.translations[0].short_description,
                    total_places=total_places,
                    m_to_start_place=distance_meters,
                )
            )

        return PageReadModel(
            items=items,
            total=total,
        )
