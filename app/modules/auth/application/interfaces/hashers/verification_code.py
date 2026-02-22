from abc import (
    ABC,
    abstractmethod,
)

from app.modules.auth.application.interfaces.hashers.base import IHasher
from app.modules.users.domain.value_objects import EmailVO


class IVerificationCodeHasher(IHasher, ABC):
    @abstractmethod
    def hash(self, *, email: EmailVO, code: str) -> str: ...

    @abstractmethod
    def verify(self, *, email: EmailVO, code: str, code_hash: str) -> bool: ...
