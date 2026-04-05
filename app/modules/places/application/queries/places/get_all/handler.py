from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.get_all.query import (
    GetAllPlacesQuery,
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
            category_slug=query.category_slug,
            limit=query.limit,
            offset=query.offset,
            translation_language=query.language,
        )

        return PaginatedPlaceCardView(
            places=[
                PlaceCardView.from_read_model(place_card)
                for place_card in place_cards.items
            ],
            pagination=OffsetPagination.create(
                total=place_cards.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
