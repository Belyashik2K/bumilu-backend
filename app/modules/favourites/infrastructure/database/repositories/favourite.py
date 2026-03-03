from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database.exception_catcher import (
    sqlalchemy_exception_catcher,
)
from app.core.shared.domain.value_objects.id import (
    IdVO,
    UserIdVO,
)
from app.modules.favourites.application.interfaces.repositories.favourite import (
    IFavouriteRepository,
)
from app.modules.favourites.domain.models.favourite import Favourite
from app.modules.favourites.infrastructure.database.models import FavouriteModel


class SQLAlchemyFavouriteRepository(IFavouriteRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    @staticmethod
    def _to_entity(data: FavouriteModel) -> Favourite:
        return Favourite(
            user_id=UserIdVO.from_uuid(data.user_id),
            entity_type=data.entity_type,
            entity_id=IdVO.from_uuid(data.entity_id),
        )

    @staticmethod
    def _to_data(entity: Favourite) -> FavouriteModel:
        return FavouriteModel(
            user_id=entity.user_id.value,
            entity_type=entity.entity_type,
            entity_id=entity.entity_id.value,
        )

    @sqlalchemy_exception_catcher
    async def add_if_not_exists(
        self,
        favourite: Favourite,
    ) -> None:
        data = self._to_data(favourite)
        await self.session.merge(data)
        await self.session.flush()

    @sqlalchemy_exception_catcher
    async def remove_if_exists(
        self,
        favourite: Favourite,
    ) -> None:
        stmt = delete(
            FavouriteModel,
        ).where(
            FavouriteModel.user_id == favourite.user_id.value,
            FavouriteModel.entity_type == favourite.entity_type,
            FavouriteModel.entity_id == favourite.entity_id.value,
        )
        await self.session.execute(stmt)
        await self.session.flush()

    @sqlalchemy_exception_catcher
    async def get_all_by_user_id(
        self,
        user_id: UserIdVO,
    ) -> list[Favourite]:
        stmt = select(FavouriteModel).where(FavouriteModel.user_id == user_id.value)
        result = await self.session.execute(stmt)
        favourites = result.scalars().all()
        return [self._to_entity(favourite) for favourite in favourites]
