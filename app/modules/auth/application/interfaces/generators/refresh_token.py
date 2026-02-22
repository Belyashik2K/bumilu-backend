from abc import (
    ABC,
    abstractmethod,
)


class IRefreshTokenGenerator(ABC):
    @abstractmethod
    def generate(self) -> str: ...
