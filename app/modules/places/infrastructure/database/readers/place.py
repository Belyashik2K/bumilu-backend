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
from app.modules.places.application.queries.places.shared.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.queries.places.shared.views import (
    PlaceAddressView,
    PlaceLocationView,
    PlacePhoneView,
    PlaceView,
    PlaceWorkingHoursIntervalView,
)
from app.modules.places.infrastructure.database.models import (
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
