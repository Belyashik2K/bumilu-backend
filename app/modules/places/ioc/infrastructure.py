from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.infrastructure.config import AppConfig
from app.modules.places.application.interfaces.file_key_generator import (
    IFileKeyGenerator,
)
from app.modules.places.application.interfaces.file_storage import IFileStorage
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.infrastructure.file_key_generator import FileKeyGenerator
from app.modules.places.infrastructure.s3_file_storage import (
    S3FileStorage,
    S3FileStorageURLBuilder,
)


class PlacesInfrastructureProvider(Provider):
    @provide(scope=Scope.APP, provides=IFileKeyGenerator)
    async def file_key_generator(self) -> FileKeyGenerator:
        return FileKeyGenerator()

    @provide(scope=Scope.APP, provides=IFileStorage)
    async def file_storage(self, config: AppConfig) -> S3FileStorage:
        return S3FileStorage(
            endpoint=config.storage.s3.endpoint_url,
            bucket_name=config.storage.s3.bucket_name,
            region=config.storage.s3.region_name,
            access_key=config.storage.s3.access_key,
            secret_key=config.storage.s3.secret_key,
        )

    @provide(scope=Scope.APP, provides=IFileStorageURLBuilder)
    async def file_storage_url_builder(
        self, config: AppConfig
    ) -> IFileStorageURLBuilder:
        return S3FileStorageURLBuilder(
            public_endpoint=config.storage.s3.public_endpoint_url,
        )
