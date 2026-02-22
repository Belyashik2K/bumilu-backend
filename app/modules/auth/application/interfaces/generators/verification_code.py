from abc import (
    ABC,
    abstractmethod,
)


class IVerificationCodeGenerator(ABC):
    @abstractmethod
    def generate(self) -> str: ...
