from abc import (
    ABC,
    abstractmethod,
)


class IFileStorage(ABC):
    @abstractmethod
    async def generate_upload_url(
        self,
        file_key: str,
        content_type: str,
        expires_in: int = 3600,
    ) -> str: ...
