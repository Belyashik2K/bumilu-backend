from app.core.application.queries import IQueryHandler
from app.core.application.queries.pagination import OffsetPagination
from app.modules.favourites.application.interfaces.preview_enricher import (
    IFavouritePreviewEnricher,
)
from app.modules.favourites.application.queries.get_all_by_user.query import (
    GetAllFavouritesByUserQuery,
)
from app.modules.favourites.application.queries.get_all_by_user.view import (
    PaginatedFavouriteRecordsView,
)
from app.modules.favourites.application.queries.shared.readers import (
    IFavouriteReader,
)
from app.modules.users.application.queries.get.exceptions import UserNotFound
from app.modules.users.application.queries.shared.readers import IUserReader


class GetAllFavouritesByUserQueryHandler(
    IQueryHandler[
        GetAllFavouritesByUserQuery,
        PaginatedFavouriteRecordsView,
    ]
):
    def __init__(
        self,
        favourite_reader: IFavouriteReader,
        user_reader: IUserReader,
        preview_enricher: IFavouritePreviewEnricher,
    ) -> None:
        self._favourite_reader = favourite_reader
        self._user_reader = user_reader
        self._preview_enricher = preview_enricher

    async def handle(
        self, query: GetAllFavouritesByUserQuery
    ) -> PaginatedFavouriteRecordsView:
        user = await self._user_reader.get_by_id(query.user_id)
        if not user:
            raise UserNotFound(user_id=query.user_id)  # type: ignore

        favourite_records = await self._favourite_reader.get_favourites_by_user_id(
            user_id=query.user_id,
            limit=query.limit,
            offset=query.offset,
            entity_type=query.entity_type,
        )

        enriched_favourites = await self._preview_enricher.enrich(
            items=favourite_records.items,
            translation_language=query.language,
        )

        return PaginatedFavouriteRecordsView(
            user_id=query.user_id,
            favourites=enriched_favourites,
            pagination=OffsetPagination.create(
                limit=query.limit,
                offset=query.offset,
                total=favourite_records.total,
            ),
        )
