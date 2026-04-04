from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favourites.application.queries.get_all_by_user.view import (
    FavouritesPage,
)
from app.modules.favourites.application.queries.shared.readers import (
    IFavouriteReader,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum


class SQLAlchemyFavouriteReader(IFavouriteReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_favourites_by_user_id(
        self,
        user_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
        entity_type: FavouriteEntityTypeEnum | None = None,
    ) -> FavouritesPage:
        raise NotImplementedError("This method is not implemented yet")
        # count_stmt = (
        #     select(func.count())
        #     .select_from(FavouriteModel)
        #     .where(FavouriteModel.user_id == user_id)
        # )
        # items_stmt = select(FavouriteModel).where(FavouriteModel.user_id == user_id)
        #
        # if entity_type is not None:
        #     count_stmt = count_stmt.where(FavouriteModel.entity_type == entity_type)
        #     items_stmt = items_stmt.where(FavouriteModel.entity_type == entity_type)
        #
        # total_subquery = count_stmt.scalar_subquery()
        # stmt = (
        #     items_stmt.add_columns(total_subquery.label("total_count"))
        #     .order_by(FavouriteModel.created_at.desc())
        #     .limit(limit)
        #     .offset(offset)
        # )
        #
        # result = await self._session.execute(stmt)
        # rows = result.all()
        #
        # if not rows:
        #     total = await self._session.scalar(count_stmt)
        #     return FavouritesPage(
        #         items=[],
        #         total=total or 0,
        #     )
        #
        # favourites: list[FavouriteModel] = [row.FavouriteModel for row in rows]
        # total = rows[0].total_count
        #
        # return FavouritesPage(
        #     items=[
        #         FavouriteView(
        #             entity=FavouriteEntityInfoView(
        #                 id=fav.entity_id,
        #                 type=fav.entity_type,
        #             ),
        #             created_at=fav.created_at,
        #         )
        #         for fav in favourites
        #     ],
        #     total=total or 0,
        # )
