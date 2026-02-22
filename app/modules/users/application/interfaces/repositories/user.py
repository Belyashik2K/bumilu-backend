from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.modules.users.domain.models.user import User


class IUserRepository(IBaseRepository[User], ABC): ...
