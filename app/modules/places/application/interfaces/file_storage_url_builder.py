from abc import (
    ABC,
    abstractmethod,
)


class IFileStorageURLBuilder(ABC):
    @abstractmethod
    def build_file_url(self, file_key: str | None) -> str | None: ...
