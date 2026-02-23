from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.shared.domain.value_objects.id import (
    DeviceIdVO,
    UserIdVO,
)
from app.modules.auth.application.interfaces.repositories.device import (
    IDeviceRepository,
)
from app.modules.auth.domain.models.device import Device
from app.modules.auth.infrastructure.database.models import DeviceModel


class SQLAlchemyDeviceRepository(
    IDeviceRepository, SQLAlchemyBaseRepository[Device, DeviceModel]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DeviceModel)

    def _to_entity(self, data: DeviceModel) -> Device:
        return Device(
            id=DeviceIdVO.from_uuid(data.id),
            platform=data.platform,
            name=data.name,
            app_version=data.app_version,
            guest_user_id=UserIdVO.from_uuid(data.guest_user_id)
            if data.guest_user_id
            else None,
            last_seen_at=data.last_seen_at,
        )

    def _to_data(self, entity: Device) -> DeviceModel:
        return DeviceModel(
            id=entity.id.value,
            platform=entity.platform,
            name=entity.name,
            app_version=entity.app_version,
            guest_user_id=entity.guest_user_id.value if entity.guest_user_id else None,
            last_seen_at=entity.last_seen_at,
        )
