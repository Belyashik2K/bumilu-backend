from abc import ABC

from app.core.application.interfaces.repositories import IBaseRepository
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.users.domain.models.user import User


class IUserRepository(IBaseRepository[User, UserIdVO], ABC): ...
