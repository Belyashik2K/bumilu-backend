from abc import (
    ABC,
    abstractmethod,
)


class IHasher(ABC):
    @abstractmethod
    def hash(self, *args, **kwargs) -> str: ...

    @abstractmethod
    def verify(self, *args, **kwargs) -> bool: ...
