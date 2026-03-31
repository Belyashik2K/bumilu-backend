from uuid import UUID

from sqlalchemy import (
    and_,
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
    ) -> PlaceView:
        return PlaceView(
            id=place.id,
            category_id=place.category_id,
            title=place.translations[0].title,
            description=place.translations[0].description,
            short_description=place.translations[0].short_description,
            timezone=place.timezone,
            location=PlaceLocationView(
                latitude=place.latitude,
                longitude=place.longitude,
            ),
            address=PlaceAddressView(
                display=place.translations[0].address_display,
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
            working_hours={
                day: [
                    PlaceWorkingHoursIntervalView(
                        start=wh.start_time,
                        end=wh.end_time,
                    )
                    for wh in place.working_hours
                    if wh.weekday == day
                ]
                for day in range(7)
            },
        )

    async def get_by_id(
        self, place_id: UUID, translation_language: LanguageEnum
    ) -> PlaceView | None:
        stmt = (
            select(PlaceModel)
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
        place = result.scalars().first()
        if place is None:
            return None
        return self.to_view(place)
