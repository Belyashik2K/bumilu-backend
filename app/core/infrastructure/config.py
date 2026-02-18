from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource,
)


class DocsConfig(BaseModel):
    title: str
    description: str
    version: str
    openapi_url: str
    redoc_url: str
    swagger_url: str


class RunConfig(BaseModel):
    host: str
    port: int


class CORSConfig(BaseModel):
    enabled: bool
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=("config.yaml", "config.dev.yaml"),
        env_file=(".env", ".env.dev"),
        env_nested_delimiter="__",
        extra="ignore",
    )

    docs: DocsConfig
    run: RunConfig
    cors: CORSConfig

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
            init_settings
        )
