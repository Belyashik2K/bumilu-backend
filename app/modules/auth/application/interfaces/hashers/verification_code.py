from abc import (
    ABC,
    abstractmethod,
)

from app.modules.auth.application.interfaces.hashers.base import IHasher
from app.modules.users.domain.value_objects import UserEmailVO


class IVerificationCodeHasher(IHasher, ABC):
    @abstractmethod
    def hash(self, *, email: UserEmailVO, code: str) -> str: ...

    @abstractmethod
    def verify(self, *, email: UserEmailVO, code: str, code_hash: str) -> bool: ...
