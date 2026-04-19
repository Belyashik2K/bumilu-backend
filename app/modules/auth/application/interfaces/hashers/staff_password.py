from abc import (
    ABC,
    abstractmethod,
)

from app.modules.auth.application.interfaces.hashers.base import IHasher


class IStaffPasswordHasher(IHasher, ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool: ...
