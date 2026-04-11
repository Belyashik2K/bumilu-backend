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
from sqlalchemy.orm import selectinload

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceIdVO,
    PlacePhoneIdVO,
)
from app.core.domain.value_objects.location import LocationVO
from app.core.infrastructure.database.exception_catcher import (
    sqlalchemy_exception_catcher,
)
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.domain.places.models.place.model import Place
from app.modules.places.domain.places.models.place_phone.model import PlacePhone
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)
from app.modules.places.domain.places.value_objects.taxi_address.object import (
    PlaceTaxiAddressVO,
)
from app.modules.places.domain.places.value_objects.timezone.object import TimezoneVO
from app.modules.places.infrastructure.database.models import (
    PlaceModel,
    PlacePhoneModel,
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
        return LocationVO(latitude=point.y, longitude=point.x)  # type: ignore[arg-type]

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

    def _to_entity_core(self, model: PlaceModel) -> Place:
        return Place(
            id=PlaceIdVO.from_uuid(model.id),
            category_id=PlaceCategoryIdVO(model.category_id),
            location=self.wkb_to_location_vo(model.location),
            timezone=TimezoneVO(model.timezone),
            address_taxi=PlaceTaxiAddressVO(model.address_taxi),
            address_taxi_comment=model.address_taxi_comment,
            status=model.status,
            translation_language_codes=set(model.translation_language_codes or []),
            phones=[],
        )

    def _to_entity_with_phones(self, model: PlaceModel) -> Place:
        entity = self._to_entity_core(model)
        entity.phones = [self._phone_to_entity(phone) for phone in model.phones]
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
                    self._phone_to_model(
                        entity_phone,
                        place_id=entity.id,
                    )
                )
                continue

            model_phone.number = entity_phone.number.value
            model_phone.type = entity_phone.type
            model_phone.is_primary = entity_phone.is_primary

    @sqlalchemy_exception_catcher
    async def get_by_id(self, place_id: PlaceIdVO) -> Place | None:
        stmt = select(PlaceModel).where(PlaceModel.id == place_id.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return self._to_entity_core(model)

    @sqlalchemy_exception_catcher
    async def get_by_id_with_phones(self, place_id: PlaceIdVO) -> Place | None:
        stmt = (
            select(PlaceModel)
            .where(PlaceModel.id == place_id.value)
            .options(selectinload(PlaceModel.phones))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return self._to_entity_with_phones(model)

    @sqlalchemy_exception_catcher
    async def save(self, entity: Place) -> Place:
        stmt = (
            select(PlaceModel)
            .where(PlaceModel.id == entity.id.value)
            .options(selectinload(PlaceModel.phones))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = self._to_model(entity)
            model.phones = [
                self._phone_to_model(phone, place_id=entity.id)
                for phone in entity.phones
            ]
            self.session.add(model)
            await self.session.flush()
            return self._to_entity_with_phones(model)

        self._update_model(model, entity)
        self._sync_phones(model, entity)

        await self.session.flush()
        return self._to_entity_with_phones(model)

    @sqlalchemy_exception_catcher
    async def delete_by_id(self, place_id: PlaceIdVO) -> None:
        stmt = delete(PlaceModel).where(PlaceModel.id == place_id.value)
        await self.session.execute(stmt)
        await self.session.flush()
