from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.auth.domain.models.device import Device


class IDeviceRepository(IBaseRepository[Device], ABC): ...
