from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import DeviceIdVO
from app.modules.auth.domain.models.device import Device


class IDeviceRepository(IBaseRepository[Device, DeviceIdVO], ABC): ...
