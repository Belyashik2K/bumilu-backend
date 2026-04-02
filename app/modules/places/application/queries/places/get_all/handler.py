from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.places.get_all.query import (
    GetAllPlacesQuery,
)
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.utils.working_hours import (
    extract_today_working_hours,
)
from app.modules.places.application.queries.places.shared.views import (
    PaginatedPlaceCardView,
    PlaceCardView,
)


class GetAllPlacesQueryHandler(
    IQueryHandler[GetAllPlacesQuery, PaginatedPlaceCardView]
):
    def __init__(
        self,
        place_reader: IPlaceReader,
    ) -> None:
        self._place_reader = place_reader

    async def handle(self, query: GetAllPlacesQuery) -> PaginatedPlaceCardView:
        place_cards = await self._place_reader.get_all(
            title_like=query.title_like,
            category_id=query.category_id,
            limit=query.limit,
            offset=query.offset,
            translation_language=query.language,
        )

        views = [
            PlaceCardView(
                id=place_card.id,
                title=place_card.title,
                short_description=place_card.short_description,
                timezone=place_card.timezone,
                category=place_card.category,
                location=place_card.location,
                rating=place_card.rating,
                today_working_hours=extract_today_working_hours(
                    timezone=place_card.timezone,
                    working_hours=place_card.working_hours,
                ),
            )
            for place_card in place_cards.items
        ]

        return PaginatedPlaceCardView(
            places=views,
            pagination=OffsetPagination.create(
                total=place_cards.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
