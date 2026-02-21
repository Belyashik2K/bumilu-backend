from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class DocsConfig(BaseModel):
    title: str
    description: str
    version: str
    openapi_url: str
    redoc_url: str
    swagger_url: str


class DatabaseConfig(BaseModel):
    type: str
    user: str
    password: str
    host: str
    port: int
    name: str
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    @property
    def dsn(self) -> str:
        return f"{self.type}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class CORSConfig(BaseModel):
    enabled: bool
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


class RunConfig(BaseModel):
    host: str
    port: int


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=("config.yaml", "config.dev.yaml"),
        env_file=(".env", ".env.dev"),
        env_nested_delimiter="__",
        extra="ignore",
    )

    docs: DocsConfig
    database: DatabaseConfig
    cors: CORSConfig
    run: RunConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
            init_settings,
        )
