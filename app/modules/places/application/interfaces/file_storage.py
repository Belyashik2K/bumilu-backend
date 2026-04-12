from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class FileObjectInfo:
    file_key: str
    content_type: str | None = field(default=None)
    size: int | None = field(default=None)


class IFileStorage(ABC):
    @abstractmethod
    async def generate_upload_url(
        self,
        file_key: str,
        content_type: str,
        expires_in: int = 3600,
    ) -> str: ...

    @abstractmethod
    async def get_object_info(
        self,
        *,
        file_key: str,
    ) -> FileObjectInfo | None: ...
