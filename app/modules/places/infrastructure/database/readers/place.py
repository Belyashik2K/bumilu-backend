from uuid import UUID

from sqlalchemy import (
    Float,
    and_,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    contains_eager,
    selectinload,
)

from app.core.enums import LanguageEnum
from app.core.utils.datetime import get_current_dt_in_timezone
from app.modules.places.application.queries.places.get_map_poi.query import BBox
from app.modules.places.application.queries.places.shared.models.place_address import (
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    PlaceDetailsReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    PlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_hour import (
    PlaceWorkingHourReadModel,
)
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import (
    PlaceCardCategoryView,
    PlaceCardPage,
    PlaceCardView,
    PlaceLocationView,
    PlaceMapPOICategoryView,
    PlaceMapPOIView,
    PlaceRatingView,
    PlaceWorkingHoursIntervalView,
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

    @staticmethod
    def to_card_view(
        place: PlaceModel,
        *,
        rating_average: int | None = None,
        reviews_count: int | None = None,
    ) -> PlaceCardView:
        translation = place.translations[0]

        today_working_hours = []
        for wh in place.working_hours:
            now = get_current_dt_in_timezone(place.timezone)
            if wh.weekday == now.weekday() + 1:
                today_working_hours.append(
                    PlaceWorkingHoursIntervalView(
                        start=wh.start_time,
                        end=wh.end_time,
                    )
                )

        return PlaceCardView(
            id=place.id,
            title=translation.title,
            short_description=translation.short_description,
            timezone=place.timezone,
            category=PlaceCardCategoryView(
                name=place.category.translations[0].name,
            ),
            rating=PlaceRatingView(reviews_count=reviews_count, average=rating_average),
            location=PlaceLocationView(
                latitude=place.latitude,
                longitude=place.longitude,
            ),
            today_working_hours=today_working_hours,
        )

    @staticmethod
    async def to_map_poi_view(
        place: PlaceModel,
    ) -> PlaceMapPOIView:
        place_translation = place.translations[0]
        category_translation = place.category.translations[0]

        return PlaceMapPOIView(
            id=place.id,
            title=place_translation.title,
            category=PlaceMapPOICategoryView(
                id=place.category.id,
                name=category_translation.name,
                icon_key=place.category.icon_key,
                marker_color=place.category.marker_color,
            ),
            location=PlaceLocationView(
                latitude=place.latitude,
                longitude=place.longitude,
            ),
        )

    async def get_by_id(
        self,
        place_id: UUID,
        translation_language: LanguageEnum,
    ) -> PlaceDetailsReadModel | None:
        stmt = (
            select(
                PlaceModel,
            )
            .join(PlaceModel.translations)
            .where(
                and_(
                    PlaceTranslationModel.language_code == translation_language,
                    PlaceModel.id == place_id,
                )
            )
            .options(
                contains_eager(PlaceModel.translations),
                selectinload(PlaceModel.phones),
                selectinload(PlaceModel.working_hours),
            )
        )

        result = await self._session.execute(stmt)
        place = result.unique().scalar_one_or_none()

        if place is None:
            return None

        translation = place.translations[0]

        return PlaceDetailsReadModel(
            id=place.id,
            category_id=place.category_id,
            title=translation.title,
            description=translation.description,
            short_description=translation.short_description,
            timezone=place.timezone,
            location=PlaceLocationReadModel(
                latitude=place.latitude,
                longitude=place.longitude,
            ),
            address=PlaceAddressReadModel(
                display=translation.address_display,
                taxi=place.address_taxi,
                taxi_comment=place.address_taxi_comment,
            ),
            rating=PlaceRatingReadModel(
                reviews_count=place.rating_reviews_count, average=place.rating_average
            ),
            phones=[
                PlacePhoneReadModel(
                    number=phone.number,
                    type=phone.type,
                    primary=phone.is_primary,
                )
                for phone in place.phones
            ],
            working_hours=[
                PlaceWorkingHourReadModel(
                    weekday=wh.weekday,
                    start_time=wh.start_time,
                    end_time=wh.end_time,
                )
                for wh in place.working_hours
            ],
        )

    async def get_all(
        self,
        *,
        title_like: str | None,
        category_id: UUID | None,
        translation_language: LanguageEnum,
        limit: int,
        offset: int,
    ) -> PlaceCardPage:
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

        if category_id:
            base_filters.append(PlaceModel.category_id == category_id)

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
            return PlaceCardPage(items=[], total=total or 0)

        total = rows[0].total_count or 0

        items = []
        for place, rating_average, reviews_count, _ in rows:
            items.append(
                self.to_card_view(
                    place,
                    rating_average=rating_average,
                    reviews_count=reviews_count,
                )
            )

        return PlaceCardPage(
            items=items,
            total=total,
        )

    async def list_poi_in_bounds(
        self,
        *,
        bounds: BBox,
        translation_language: LanguageEnum,
        limit: int,
    ) -> list[PlaceMapPOIView]:
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

        items: list[PlaceMapPOIView] = [
            await self.to_map_poi_view(
                place=row.PlaceModel,
            )
            for row in rows
        ]

        return items
