from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.auth.domain.models.principal import Principal


class IPrincipalRepository(IBaseRepository[Principal], ABC): ...
