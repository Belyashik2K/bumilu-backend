from app.core.application.queries import IQueryHandler
from app.core.shared.application.queries.pagination import OffsetPagination
from app.modules.favourites.application.queries.get_all_by_user.query import (
    GetAllFavouritesByUserQuery,
)
from app.modules.favourites.application.queries.get_all_by_user.view import (
    PaginatedFavouritesView,
)
from app.modules.favourites.application.queries.readers.favourite import (
    IFavouriteReader,
)
from app.modules.users.application.queries.get.exceptions import UserNotFound
from app.modules.users.application.queries.readers.user import IUserReader


class GetAllFavouritesByUserQueryHandler(
    IQueryHandler[
        GetAllFavouritesByUserQuery,
        PaginatedFavouritesView,
    ]
):
    def __init__(
        self,
        favourite_reader: IFavouriteReader,
        user_reader: IUserReader,
    ) -> None:
        self._favourite_reader = favourite_reader
        self._user_reader = user_reader

    async def handle(
        self, query: GetAllFavouritesByUserQuery
    ) -> PaginatedFavouritesView:
        user = await self._user_reader.get_by_id(query.user_id)
        if not user:
            raise UserNotFound(user_id=query.user_id)  # type: ignore

        favourites = await self._favourite_reader.get_favourites_by_user_id(
            user_id=query.user_id,
            limit=query.limit,
            offset=query.offset,
            entity_type=query.entity_type,
        )

        return PaginatedFavouritesView(
            user_id=query.user_id,
            favourites=favourites.items,
            pagination=OffsetPagination.create(
                limit=query.limit,
                offset=query.offset,
                total=favourites.total,
            ),
        )
