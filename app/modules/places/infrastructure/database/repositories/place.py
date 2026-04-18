from time import time
from uuid import UUID

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import (
    from_shape,
    to_shape,
)
from shapely.geometry import Point
from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
)
from sqlalchemy.orm.interfaces import ORMOption

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceIdVO,
    PlacePhoneIdVO,
    PlacePhotoIdVO,
    PlaceWorkingDayIdVO,
)
from app.core.domain.value_objects.location import LocationVO
from app.core.infrastructure.database.exception_catcher import (
    sqlalchemy_exception_catcher,
)
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
    PlaceLoadOptions,
)
from app.modules.places.domain.places.models.place.model import Place
from app.modules.places.domain.places.models.place_phone.model import PlacePhone
from app.modules.places.domain.places.models.place_photo.model import PlacePhoto
from app.modules.places.domain.places.models.place_working_day.model import (
    PlaceWorkingDay,
)
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)
from app.modules.places.domain.places.value_objects.taxi_address.object import (
    PlaceTaxiAddressVO,
)
from app.modules.places.domain.places.value_objects.timezone.object import TimezoneVO
from app.modules.places.domain.places.value_objects.weekday.object import WeekdayVO
from app.modules.places.domain.places.value_objects.working_interval.object import (
    WorkingIntervalVO,
)
from app.modules.places.infrastructure.database.models import (
    PlaceModel,
    PlacePhoneModel,
    PlacePhotoModel,
    PlaceWorkingDayModel,
    PlaceWorkingHourModel,
)
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


class SQLAlchemyPlaceRepository(IPlaceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def location_vo_to_wkb(location: LocationVO) -> WKBElement:
        point = Point(location.longitude, location.latitude)
        return from_shape(point, srid=4326)  # type: ignore[arg-type]

    @staticmethod
    def wkb_to_location_vo(wkb: WKBElement) -> LocationVO:
        point = to_shape(wkb)
        return LocationVO(latitude=point.y, longitude=point.x)  # type: ignore[type-var]

    @staticmethod
    def _build_load_options(options: PlaceLoadOptions) -> list[ORMOption]:
        loaders: list[ORMOption] = []

        if options.phones:
            loaders.append(selectinload(PlaceModel.phones))

        if options.working_days:
            loaders.append(
                selectinload(PlaceModel.working_days).selectinload(
                    PlaceWorkingDayModel.working_hours
                )
            )

        if options.photos:
            loaders.append(selectinload(PlaceModel.photos))

        return loaders

    def _build_save_load_options(self, entity: Place) -> list[ORMOption]:
        return self._build_load_options(
            PlaceLoadOptions(
                phones=entity.phones is not None,
                working_days=entity.working_days is not None,
                photos=entity.photos is not None,
            )
        )

    @staticmethod
    def _phone_to_model(
        phone: PlacePhone,
        *,
        place_id: PlaceIdVO,
    ) -> PlacePhoneModel:
        return PlacePhoneModel(
            id=phone.id.value,
            place_id=place_id.value,
            number=phone.number.value,
            type=phone.type,
            is_primary=phone.is_primary,
        )

    @staticmethod
    def _phone_to_entity(model: PlacePhoneModel) -> PlacePhone:
        return PlacePhone(
            id=PlacePhoneIdVO.from_uuid(model.id),
            number=PlacePhoneNumberVO(model.number),
            type=model.type,
            is_primary=model.is_primary,
        )

    @staticmethod
    def _photo_to_model(
        photo: PlacePhoto,
        *,
        place_id: PlaceIdVO,
    ) -> PlacePhotoModel:
        return PlacePhotoModel(
            id=photo.id.value,
            place_id=place_id.value,
            file_key=photo.file_key,
            thumbnail_file_key=photo.thumbnail_file_key,
            status=photo.status,
        )

    @staticmethod
    def _photo_to_entity(model: PlacePhotoModel) -> PlacePhoto:
        return PlacePhoto(
            id=PlacePhotoIdVO.from_uuid(model.id),
            file_key=model.file_key,
            thumbnail_file_key=model.thumbnail_file_key,
            status=model.status,
        )

    @staticmethod
    def _working_hour_to_model(interval: WorkingIntervalVO) -> PlaceWorkingHourModel:
        return PlaceWorkingHourModel(
            start_time=interval.start_time,
            end_time=interval.end_time,
        )

    @staticmethod
    def _working_hour_to_entity(model: PlaceWorkingHourModel) -> WorkingIntervalVO:
        return WorkingIntervalVO(
            start_time=model.start_time,
            end_time=model.end_time,
        )

    def _working_day_to_model(
        self,
        day: PlaceWorkingDay,
        *,
        place_id: PlaceIdVO,
    ) -> PlaceWorkingDayModel:
        model = PlaceWorkingDayModel(
            id=day.id.value,
            place_id=place_id.value,
            weekday=day.weekday.value,
            status=day.status,
        )
        model.working_hours = [
            self._working_hour_to_model(interval) for interval in day.intervals
        ]
        return model

    def _working_day_to_entity(self, model: PlaceWorkingDayModel) -> PlaceWorkingDay:
        return PlaceWorkingDay(
            id=PlaceWorkingDayIdVO.from_uuid(model.id),
            weekday=WeekdayVO(value=model.weekday),
            status=model.status,
            intervals=[
                self._working_hour_to_entity(interval)
                for interval in model.working_hours
            ],
        )

    def _to_model(self, entity: Place) -> PlaceModel:
        return PlaceModel(
            id=entity.id.value,
            category_id=entity.category_id.value,
            location=self.location_vo_to_wkb(entity.location),
            timezone=entity.timezone.value,
            address_taxi=entity.address_taxi.value,
            address_taxi_comment=entity.address_taxi_comment,
            status=entity.status,
        )

    def _update_model(self, model: PlaceModel, entity: Place) -> None:
        model.category_id = entity.category_id.value
        model.location = self.location_vo_to_wkb(entity.location)
        model.timezone = entity.timezone.value
        model.address_taxi = entity.address_taxi.value
        model.address_taxi_comment = entity.address_taxi_comment
        model.status = entity.status

    def _to_entity(
        self,
        model: PlaceModel,
        *,
        options: PlaceLoadOptions,
    ) -> Place:
        entity = Place(
            id=PlaceIdVO.from_uuid(model.id),
            category_id=PlaceCategoryIdVO.from_uuid(model.category_id),
            location=self.wkb_to_location_vo(model.location),
            timezone=TimezoneVO(model.timezone),
            address_taxi=PlaceTaxiAddressVO(model.address_taxi),
            address_taxi_comment=model.address_taxi_comment,
            status=model.status,
            translation_language_codes=set(model.translation_language_codes or []),
            phones=[] if options.phones else None,
            working_days=[] if options.working_days else None,
            photos=[] if options.photos else None,
        )

        if options.phones:
            entity.phones = [self._phone_to_entity(phone) for phone in model.phones]

        if options.working_days:
            entity.working_days = [
                self._working_day_to_entity(day) for day in model.working_days
            ]

        if options.photos:
            entity.photos = [self._photo_to_entity(photo) for photo in model.photos]

        return entity

    def _sync_phones(self, model: PlaceModel, entity: Place) -> None:
        existing_by_id: dict[UUID, PlacePhoneModel] = {
            phone.id: phone for phone in model.phones
        }
        incoming_by_id: dict[UUID, PlacePhone] = {
            phone.id.value: phone for phone in entity.phones
        }

        for model_phone in list(model.phones):
            if model_phone.id not in incoming_by_id:
                model.phones.remove(model_phone)

        for entity_phone in entity.phones:
            model_phone = existing_by_id.get(entity_phone.id.value)
            if model_phone is None:
                model.phones.append(
                    self._phone_to_model(entity_phone, place_id=entity.id)
                )
                continue

            model_phone.number = entity_phone.number.value
            model_phone.type = entity_phone.type
            model_phone.is_primary = entity_phone.is_primary

    def _sync_photos(self, model: PlaceModel, entity: Place) -> None:
        existing_by_id: dict[UUID, PlacePhotoModel] = {
            photo.id: photo for photo in model.photos
        }
        incoming_by_id: dict[UUID, PlacePhoto] = {
            photo.id.value: photo for photo in entity.photos
        }

        for model_photo in list(model.photos):
            if model_photo.id not in incoming_by_id:
                model.photos.remove(model_photo)

        for entity_photo in entity.photos:
            model_photo = existing_by_id.get(entity_photo.id.value)
            if model_photo is None:
                model.photos.append(
                    self._photo_to_model(entity_photo, place_id=entity.id)
                )
                continue

            model_photo.file_key = entity_photo.file_key
            model_photo.thumbnail_file_key = entity_photo.thumbnail_file_key
            model_photo.status = entity_photo.status

    def _sync_working_hours(
        self,
        model_day: PlaceWorkingDayModel,
        entity_day: PlaceWorkingDay,
    ) -> None:
        existing_by_key: dict[tuple[time, time], PlaceWorkingHourModel] = {
            (hour.start_time, hour.end_time): hour for hour in model_day.working_hours
        }

        incoming_intervals_by_key: dict[tuple[time, time], WorkingIntervalVO] = {
            (interval.start_time, interval.end_time): interval
            for interval in entity_day.intervals
        }
        incoming_keys = set(incoming_intervals_by_key.keys())

        for model_hour in list(model_day.working_hours):
            key = (model_hour.start_time, model_hour.end_time)
            if key not in incoming_keys:
                model_day.working_hours.remove(model_hour)

        for key, interval in incoming_intervals_by_key.items():
            if key not in existing_by_key:
                model_day.working_hours.append(self._working_hour_to_model(interval))

    def _sync_working_days(self, model: PlaceModel, entity: Place) -> None:
        existing_by_id: dict[UUID, PlaceWorkingDayModel] = {
            day.id: day for day in model.working_days
        }
        incoming_by_id: dict[UUID, PlaceWorkingDay] = {
            day.id.value: day for day in entity.working_days
        }

        for model_day in list(model.working_days):
            if model_day.id not in incoming_by_id:
                model.working_days.remove(model_day)

        for entity_day in entity.working_days:
            model_day = existing_by_id.get(entity_day.id.value)
            if model_day is None:
                model.working_days.append(
                    self._working_day_to_model(entity_day, place_id=entity.id)
                )
                continue

            model_day.weekday = entity_day.weekday.value
            model_day.status = entity_day.status

            if entity_day.status == PlaceWorkingDayStatusEnum.OPEN:
                self._sync_working_hours(model_day, entity_day)
            else:
                model_day.working_hours.clear()

    @sqlalchemy_exception_catcher
    async def get_by_id(
        self,
        place_id: PlaceIdVO,
        *,
        options: PlaceLoadOptions | None = None,
    ) -> Place | None:
        options = options or PlaceLoadOptions()

        stmt = (
            select(PlaceModel)
            .where(PlaceModel.id == place_id.value)
            .options(*self._build_load_options(options))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return self._to_entity(model, options=options)

    @sqlalchemy_exception_catcher
    async def save(self, entity: Place) -> Place:
        load_options = self._build_save_load_options(entity)

        stmt = (
            select(PlaceModel)
            .where(PlaceModel.id == entity.id.value)
            .options(*load_options)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = self._to_model(entity)

            if entity.phones is not None:
                model.phones = [
                    self._phone_to_model(phone, place_id=entity.id)
                    for phone in entity.phones
                ]

            if entity.working_days is not None:
                model.working_days = [
                    self._working_day_to_model(day, place_id=entity.id)
                    for day in entity.working_days
                ]

            if entity.photos is not None:
                model.photos = [
                    self._photo_to_model(photo, place_id=entity.id)
                    for photo in entity.photos
                ]

            self.session.add(model)
            await self.session.flush()
            await self.session.refresh(model, ["translation_language_codes"])

            return self._to_entity(
                model,
                options=PlaceLoadOptions(
                    phones=entity.phones is not None,
                    working_days=entity.working_days is not None,
                    photos=entity.photos is not None,
                ),
            )

        self._update_model(model, entity)

        if entity.phones is not None:
            self._sync_phones(model, entity)

        if entity.working_days is not None:
            self._sync_working_days(model, entity)

        if entity.photos is not None:
            self._sync_photos(model, entity)

        await self.session.flush()

        return self._to_entity(
            model,
            options=PlaceLoadOptions(
                phones=entity.phones is not None,
                working_days=entity.working_days is not None,
                photos=entity.photos is not None,
            ),
        )

    @sqlalchemy_exception_catcher
    async def delete_by_id(self, place_id: PlaceIdVO) -> None:
        stmt = delete(PlaceModel).where(PlaceModel.id == place_id.value)
        await self.session.execute(stmt)
        await self.session.flush()
