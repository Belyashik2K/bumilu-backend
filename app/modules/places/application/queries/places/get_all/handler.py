from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.places.get_all.query import (
    GetAllPlacesQuery,
)
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import (
    PaginatedPlaceCardView,
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
        place_cards = await self._place_reader.list(
            title_like=query.title_like,
            category_id=query.category_id,
            limit=query.limit,
            offset=query.offset,
            translation_language=query.language,
        )
        return PaginatedPlaceCardView(
            places=place_cards.items,
            pagination=OffsetPagination.create(
                total=place_cards.total,
                limit=query.limit,
                offset=query.offset,
            ),
        )
