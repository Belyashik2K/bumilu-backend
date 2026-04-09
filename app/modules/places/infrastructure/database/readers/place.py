from uuid import UUID

from sqlalchemy import (
    Float,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
    selectinload,
)

from app.core.application.queries.pagination import PageReadModel
from app.core.enums import LanguageEnum
from app.modules.favourites.infrastructure.database.models import PlaceFavouriteModel
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.get_map_poi.query import BBox
from app.modules.places.application.queries.places.shared.mappers import (
    PlaceReadModelMapper,
)
from app.modules.places.application.queries.places.shared.models.place_card import (
    PlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    PlaceDetailsReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_map_poi import (
    PlaceMapPOIReadModel,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceCategoryTranslationModel,
    PlaceModel,
    PlaceTranslationModel,
)
from app.modules.reviews.infrastructure.database.models import ReviewModel
from app.modules.reviews.shared.enums import ReviewEntityTypeEnum


class SQLAlchemyPlaceReader(IPlaceReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists(self, place_id: UUID) -> bool:
        stmt = (
            select(func.count())
            .select_from(PlaceModel)
            .where(PlaceModel.id == place_id)
        )
        result = await self._session.execute(stmt)
        count = result.scalar_one()
        return count > 0

    async def count_by_category_id(self, category_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(PlaceModel)
            .where(PlaceModel.category_id == category_id)
        )
        result = await self._session.execute(stmt)
        count = result.scalar_one()
        return count

    async def get_by_id(
        self,
        *,
        actor_id: UUID | None = None,
        place_id: UUID,
        translation_language: LanguageEnum,
    ) -> PlaceDetailsReadModel | None:
        is_favorite_subquery = (
            select(PlaceFavouriteModel.user_id)
            .where(
                PlaceFavouriteModel.place_id == PlaceModel.id,
                PlaceFavouriteModel.user_id == actor_id,
            )
            .exists()
        )

        stmt = (
            select(
                PlaceModel,
                is_favorite_subquery.label("is_favorite"),
            )
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .where(
                PlaceTranslationModel.language_code == translation_language,
                PlaceCategoryTranslationModel.language_code == translation_language,
                PlaceModel.id == place_id,
            )
            .options(
                selectinload(PlaceModel.phones),
                selectinload(PlaceModel.working_hours),
                contains_eager(PlaceModel.translations),
                contains_eager(PlaceModel.category).contains_eager(
                    PlaceCategoryModel.translations
                ),
            )
        )

        result = await self._session.execute(stmt)
        place, is_favorite = result.unique().one()

        if place is None:
            return None
        return PlaceReadModelMapper.map_details(place=place, is_favorite=is_favorite)

    async def get_cards_by_ids(
        self,
        place_ids: list[UUID],
        translation_language: LanguageEnum,
    ) -> list[PlaceCardReadModel]:
        if not place_ids:
            return []

        reviews_subq = (
            select(
                ReviewModel.entity_id.label("place_id"),
                func.avg(ReviewModel.rating).cast(Float).label("rating_average"),
                func.count(ReviewModel.id).label("reviews_count"),
            )
            .where(
                ReviewModel.entity_type == ReviewEntityTypeEnum.PLACE,
                ReviewModel.entity_id.in_(place_ids),
            )
            .group_by(ReviewModel.entity_id)
            .subquery()
        )

        stmt = (
            select(
                PlaceModel,
                reviews_subq.c.rating_average,
                func.coalesce(reviews_subq.c.reviews_count, 0).label("reviews_count"),
            )
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .outerjoin(reviews_subq, reviews_subq.c.place_id == PlaceModel.id)
            .where(
                PlaceModel.id.in_(place_ids),
                PlaceTranslationModel.language_code == translation_language,
                PlaceCategoryTranslationModel.language_code == translation_language,
            )
            .options(
                selectinload(PlaceModel.working_hours),
                contains_eager(PlaceModel.translations),
                contains_eager(PlaceModel.category).contains_eager(
                    PlaceCategoryModel.translations
                ),
            )
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        cards_by_id: dict[UUID, PlaceCardReadModel] = {
            place.id: PlaceReadModelMapper.map_card(
                place=place,
                rating_average=rating_average,
                reviews_count=reviews_count,
            )
            for place, rating_average, reviews_count in rows
        }

        return [
            cards_by_id[place_id] for place_id in place_ids if place_id in cards_by_id
        ]

    async def get_all(
        self,
        *,
        title_like: str | None,
        category_slug: str | None,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PageReadModel[PlaceCardReadModel]:
        base_filters = [
            PlaceTranslationModel.language_code == translation_language,
            PlaceCategoryTranslationModel.language_code == translation_language,
        ]

        if title_like:
            base_filters.append(
                PlaceModel.translations.any(
                    PlaceTranslationModel.title.ilike(f"%{title_like}%")
                )
            )

        if category_slug:
            base_filters.append(PlaceCategoryModel.slug == category_slug)

        reviews_subq = (
            select(
                ReviewModel.entity_id.label("place_id"),
                func.avg(ReviewModel.rating).cast(Float).label("rating_average"),
                func.count(ReviewModel.id).label("reviews_count"),
            )
            .where(ReviewModel.entity_type == ReviewEntityTypeEnum.PLACE)
            .group_by(ReviewModel.entity_id)
            .subquery()
        )

        items_stmt = (
            select(
                PlaceModel,
                reviews_subq.c.rating_average,
                func.coalesce(reviews_subq.c.reviews_count, 0).label("reviews_count"),
            )
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .outerjoin(reviews_subq, reviews_subq.c.place_id == PlaceModel.id)
            .where(*base_filters)
            .options(
                selectinload(PlaceModel.working_hours),
                contains_eager(PlaceModel.translations),
                contains_eager(PlaceModel.category).contains_eager(
                    PlaceCategoryModel.translations
                ),
            )
        )

        count_stmt = (
            select(func.count(func.distinct(PlaceModel.id)))
            .select_from(PlaceModel)
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .where(*base_filters)
        )

        total_subquery = count_stmt.scalar_subquery()

        stmt = (
            items_stmt.add_columns(total_subquery.label("total_count"))
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        if not rows:
            total = await self._session.scalar(count_stmt)
            return PageReadModel(items=[], total=total or 0)

        total = rows[0].total_count or 0

        return PageReadModel(
            items=[
                PlaceReadModelMapper.map_card(
                    place=place,
                    rating_average=rating_average,
                    reviews_count=reviews_count,
                )
                for place, rating_average, reviews_count, _ in rows
            ],
            total=total,
        )

    async def list_poi_in_bounds(
        self,
        *,
        bounds: BBox,
        translation_language: LanguageEnum,
        limit: int,
    ) -> list[PlaceMapPOIReadModel]:
        bbox = func.ST_MakeEnvelope(
            bounds.west,
            bounds.south,
            bounds.east,
            bounds.north,
            4326,
        )

        stmt = (
            select(
                PlaceModel,
            )
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
            .where(
                PlaceTranslationModel.language_code == translation_language,
                PlaceCategoryTranslationModel.language_code == translation_language,
                PlaceModel.location.op("&&")(bbox),
                func.ST_Intersects(PlaceModel.location, bbox),
            )
            .options(
                contains_eager(PlaceModel.translations),
                contains_eager(PlaceModel.category).contains_eager(
                    PlaceCategoryModel.translations
                ),
            )
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        rows = result.unique().all()

        return [PlaceReadModelMapper.map_poi(place=row.PlaceModel) for row in rows]
