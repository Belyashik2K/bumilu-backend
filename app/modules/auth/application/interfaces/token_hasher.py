from abc import (
    ABC,
    abstractmethod,
)


class ITokenHasher(ABC):
    @abstractmethod
    def hash(self, token: str) -> str: ...

    @abstractmethod
    def verify(self, token: str, hashed_token: str) -> bool: ...
