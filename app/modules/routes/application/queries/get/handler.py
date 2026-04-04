from app.core.application.queries import IQueryHandler
from app.modules.places.application.queries.places.shared.utils.working_hours import (
    extract_today_working_hours,
)
from app.modules.places.application.queries.places.shared.views import PlaceCardView
from app.modules.routes.application.exceptions.route import RouteNotFound
from app.modules.routes.application.queries.get.query import GetRouteQuery
from app.modules.routes.application.queries.shared.readers.route import IRouteReader
from app.modules.routes.application.queries.shared.views import (
    RoutePointView,
    RouteView,
)


class GetRouteQueryHandler(IQueryHandler[GetRouteQuery, RouteView]):
    def __init__(
        self,
        route_reader: IRouteReader,
    ) -> None:
        self._route_reader = route_reader

    async def handle(self, query: GetRouteQuery) -> RouteView:
        route = await self._route_reader.get_by_id(
            route_id=query.route_id,
            translation_language=query.language,
        )
        if not route:
            raise RouteNotFound(route_id=query.route_id)

        return RouteView(
            id=route.id,
            title=route.title,
            description=route.description,
            short_description=route.short_description,
            points=[
                RoutePointView(
                    index=point.index,
                    preview=PlaceCardView(
                        id=point.preview.id,
                        title=point.preview.title,
                        short_description=point.preview.short_description,
                        timezone=point.preview.timezone,
                        category=point.preview.category,
                        photos=point.preview.photos[
                            :4
                        ],  # TODO: configurable number of photos
                        location=point.preview.location,
                        rating=point.preview.rating,
                        today_working_hours=extract_today_working_hours(
                            timezone=point.preview.timezone,
                            working_hours=point.preview.working_hours,
                        ),
                    ),
                )
                for point in sorted(route.points, key=lambda p: p.index)
            ],
            total_points=route.total_points,
        )
