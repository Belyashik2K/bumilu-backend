from geoalchemy2 import WKBElement
from geoalchemy2.shape import (
    from_shape,
    to_shape,
)
from shapely.geometry import Point
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceIdVO,
)
from app.core.domain.value_objects.location import LocationVO
from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.domain.places.models.place.model import Place
from app.modules.places.domain.places.value_objects.taxi_address.object import (
    TaxiAddressVO,
)
from app.modules.places.domain.places.value_objects.timezone.object import TimezoneVO
from app.modules.places.infrastructure.database.models import PlaceModel


class SQLAlchemyPlaceRepository(
    IPlaceRepository, SQLAlchemyBaseRepository[Place, PlaceModel]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PlaceModel)

    @staticmethod
    def location_vo_to_wkb(location: LocationVO) -> WKBElement:
        point = Point(location.longitude, location.latitude)
        return from_shape(point, srid=4326)  # type: ignore

    @staticmethod
    def wkb_to_location_vo(wkb: WKBElement) -> LocationVO:
        point = to_shape(wkb)
        return LocationVO(latitude=point.y, longitude=point.x)  # type: ignore

    def _to_data(self, entity: Place) -> PlaceModel:
        return PlaceModel(
            id=entity.id.value,
            category_id=entity.category_id.value,
            location=self.location_vo_to_wkb(entity.location),
            timezone=entity.timezone.value,
            address_taxi=entity.address_taxi.value,
            address_taxi_comment=entity.address_taxi_comment,
            status=entity.status,
        )

    def _to_entity(self, model: PlaceModel) -> Place:
        return Place(
            id=PlaceIdVO.from_uuid(model.id),
            category_id=PlaceCategoryIdVO(model.category_id),
            location=self.wkb_to_location_vo(model.location),
            timezone=TimezoneVO(model.timezone),
            address_taxi=TaxiAddressVO(model.address_taxi),
            address_taxi_comment=model.address_taxi_comment,
            status=model.status,
        )

    async def delete_by_id(self, place_id: PlaceIdVO) -> None:
        stmt = delete(PlaceModel).where(PlaceModel.id == place_id.value)
        await self.session.execute(stmt)
        await self.session.flush()
