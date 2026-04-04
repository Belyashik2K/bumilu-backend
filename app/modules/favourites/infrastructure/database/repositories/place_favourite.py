from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.value_objects.id import (
    IdVO,
    PrincipalIdVO,
)
from app.modules.favourites.application.interfaces.repositories.place_favourite import (
    IPlaceFavouriteRepository,
)
from app.modules.favourites.infrastructure.database.models import PlaceFavouriteModel


class SQLAlchemyPlaceFavouriteRepository(IPlaceFavouriteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_if_not_exists(
        self,
        user_id: PrincipalIdVO,
        entity_id: IdVO,
    ) -> None:
        stmt = (
            insert(PlaceFavouriteModel)
            .values(
                user_id=user_id.value,
                place_id=entity_id.value,
            )
            .on_conflict_do_nothing()
        )
        await self._session.execute(stmt)

    async def remove_if_exists(
        self,
        user_id: PrincipalIdVO,
        entity_id: IdVO,
    ) -> None:
        stmt = delete(PlaceFavouriteModel).where(
            PlaceFavouriteModel.user_id == user_id.value,
            PlaceFavouriteModel.place_id == entity_id.value,
        )
        await self._session.execute(stmt)
