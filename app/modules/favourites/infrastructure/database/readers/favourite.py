from uuid import UUID

from sqlalchemy import (
    func,
    literal,
    select,
    union_all,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Subquery

from app.core.application.queries.pagination import PageReadModel
from app.modules.favourites.application.queries.shared.models.favourite_entity import (
    RawFavouriteEntityReadModel,
)
from app.modules.favourites.application.queries.shared.models.favourite_record import (
    RawFavouriteRecordReadModel,
)
from app.modules.favourites.application.queries.shared.readers import (
    IFavouriteReader,
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
    ) -> Subquery:
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
    ) -> PageReadModel[RawFavouriteRecordReadModel]:
        favourites_subquery = self._build_favourites_union(
            user_id=user_id,
            entity_type=entity_type,
        )

        count_stmt = select(func.count()).select_from(favourites_subquery)
        total = await self._session.scalar(count_stmt) or 0

        items_stmt = (
            select(
                favourites_subquery.c.entity_id,
                favourites_subquery.c.entity_type,
                favourites_subquery.c.created_at,
            )
            .select_from(favourites_subquery)
            .order_by(favourites_subquery.c.created_at.desc())
        )

        if limit is not None:
            items_stmt = items_stmt.limit(limit)

        if offset is not None:
            items_stmt = items_stmt.offset(offset)

        result = await self._session.execute(items_stmt)
        rows = result.all()

        return PageReadModel(
            items=[
                RawFavouriteRecordReadModel(
                    entity=RawFavouriteEntityReadModel(
                        id=row.entity_id, type=FavouriteEntityTypeEnum(row.entity_type)
                    ),
                    created_at=row.created_at,
                )
                for row in rows
            ],
            total=total,
        )
