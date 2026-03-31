from uuid import UUID

from geoalchemy2 import Geometry
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
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import (
    PlaceAddressView,
    PlaceCardCategoryView,
    PlaceCardPage,
    PlaceCardView,
    PlaceLocationView,
    PlacePhoneView,
    PlaceView,
    PlaceWorkingHoursIntervalView,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceCategoryTranslationModel,
    PlaceModel,
    PlaceTranslationModel,
)


class SQLAlchemyPlaceReader(IPlaceReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def to_view(
        place: PlaceModel,
        *,
        latitude: float,
        longitude: float,
    ) -> PlaceView:
        translation = place.translations[0]

        return PlaceView(
            id=place.id,
            category_id=place.category_id,
            title=translation.title,
            description=translation.description,
            short_description=translation.short_description,
            timezone=place.timezone,
            location=PlaceLocationView(
                latitude=latitude,
                longitude=longitude,
            ),
            address=PlaceAddressView(
                display=translation.address_display,
                taxi=place.address_taxi,
                taxi_comment=place.address_taxi_comment,
            ),
            phones=[
                PlacePhoneView(
                    number=phone.number,
                    type=phone.type,
                    primary=phone.is_primary,
                )
                for phone in place.phones
            ],
            weekly_working_hours={
                str(day): [
                    PlaceWorkingHoursIntervalView(
                        start=wh.start_time,
                        end=wh.end_time,
                    )
                    for wh in place.working_hours
                    if wh.weekday == day
                ]
                for day in range(1, 8)
            },
        )

    @staticmethod
    def to_card_view(
        place: PlaceModel,
        *,
        latitude: float,
        longitude: float,
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
            location=PlaceLocationView(
                latitude=latitude,
                longitude=longitude,
            ),
            today_working_hours=today_working_hours,
        )

    async def get_by_id(
        self,
        place_id: UUID,
        translation_language: LanguageEnum,
    ) -> PlaceView | None:
        stmt = (
            select(
                PlaceModel,
                func.ST_Y(
                    PlaceModel.location.cast(Geometry(geometry_type="POINT", srid=4326))
                )
                .cast(Float)
                .label("latitude"),
                func.ST_X(
                    PlaceModel.location.cast(Geometry(geometry_type="POINT", srid=4326))
                )
                .cast(Float)
                .label("longitude"),
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
        row = result.unique().one_or_none()

        if row is None:
            return None

        place, latitude, longitude = row

        return self.to_view(
            place,
            latitude=float(latitude),
            longitude=float(longitude),
        )

    async def list(
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

        items_stmt = (
            select(
                PlaceModel,
                func.ST_Y(
                    PlaceModel.location.cast(Geometry(geometry_type="POINT", srid=4326))
                )
                .cast(Float)
                .label("latitude"),
                func.ST_X(
                    PlaceModel.location.cast(Geometry(geometry_type="POINT", srid=4326))
                )
                .cast(Float)
                .label("longitude"),
            )
            .join(PlaceModel.translations)
            .join(PlaceModel.category)
            .join(PlaceCategoryModel.translations)
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
        for place, latitude, longitude, _ in rows:
            items.append(
                self.to_card_view(
                    place,
                    latitude=float(latitude),
                    longitude=float(longitude),
                )
            )

        return PlaceCardPage(
            items=items,
            total=total,
        )
