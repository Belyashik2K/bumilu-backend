from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import (
    PaginatedView,
)
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import (
    PlaceCardView,
)
from app.modules.places.application.queries.places.user.get_all.query import (
    GetAllPlacesQuery,
)


class GetAllPlacesQueryHandler(
    IQueryHandler[GetAllPlacesQuery, PaginatedView[PlaceCardView]]
):
    def __init__(
        self, place_reader: IPlaceReader, storage_url_builder: IFileStorageURLBuilder
    ) -> None:
        self._place_reader = place_reader
        self._storage_url_builder = storage_url_builder

    async def handle(self, query: GetAllPlacesQuery) -> PaginatedView[PlaceCardView]:
        place_cards = await self._place_reader.get_all(
            title_like=query.title_like,
            category_slug=query.category_slug,
            limit=query.limit,
            offset=query.offset,
            translation_language=query.language,
        )

        return PaginatedView.create(
            items=[
                PlaceCardView.from_read_model(
                    place_card, storage_url_builder=self._storage_url_builder
                )
                for place_card in place_cards.items
            ],
            total=place_cards.total,
            limit=query.limit,
            offset=query.offset,
        )
