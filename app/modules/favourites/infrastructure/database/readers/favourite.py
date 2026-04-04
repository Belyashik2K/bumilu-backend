from uuid import UUID

from sqlalchemy import (
    func,
    literal,
    select,
    union_all,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favourites.application.queries.get_all_by_user.view import (
    FavouritesPage,
)
from app.modules.favourites.application.queries.shared.readers import (
    IFavouriteReader,
)
from app.modules.favourites.application.queries.shared.views import (
    FavouriteEntityInfoView,
    FavouriteView,
)
from app.modules.favourites.infrastructure.database.models import PlaceFavouriteModel
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class SQLAlchemyFavouriteReader(IFavouriteReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _build_favourites_union(
        user_id: UUID,
        entity_type: FavouriteEntityTypeEnum | None = None,
    ) -> select:
        place_stmt = select(
            PlaceFavouriteModel.place_id.label("entity_id"),
            literal(FavouriteEntityTypeEnum.PLACE.value).label("entity_type"),
            PlaceFavouriteModel.created_at.label("created_at"),
        ).where(PlaceFavouriteModel.user_id == user_id)

        if entity_type == FavouriteEntityTypeEnum.PLACE:
            return place_stmt.subquery("favourites_union")

        # TODO: Route favourites union when route favourites are implemented

        return union_all(place_stmt).subquery("favourites_union")

    async def get_favourites_by_user_id(
        self,
        user_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
        entity_type: FavouriteEntityTypeEnum | None = None,
    ) -> FavouritesPage:
        favourites_subquery = self._build_favourites_union(
            user_id=user_id,
            entity_type=entity_type,
        )

        count_stmt = select(func.count()).select_from(favourites_subquery)

        stmt = (
            select(
                favourites_subquery.c.entity_id,
                favourites_subquery.c.entity_type,
                favourites_subquery.c.created_at,
                count_stmt.scalar_subquery().label("total_count"),
            )
            .select_from(favourites_subquery)
            .order_by(favourites_subquery.c.created_at.desc())
        )

        if limit is not None:
            stmt = stmt.limit(limit)

        if offset is not None:
            stmt = stmt.offset(offset)

        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            total = await self._session.scalar(count_stmt)
            return FavouritesPage(items=[], total=total or 0)

        return FavouritesPage(
            items=[
                FavouriteView(
                    entity=FavouriteEntityInfoView(
                        id=row.entity_id,
                        type=FavouriteEntityTypeEnum(row.entity_type),
                    ),
                    created_at=row.created_at,
                )
                for row in rows
            ],
            total=rows[0].total_count or 0,
        )
