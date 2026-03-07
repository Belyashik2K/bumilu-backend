from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

# ======== LoggingConfig ========


class LoggingConfig(BaseModel):
    level: str
    format: str
    datetime_format: str


# ======== DocsConfig ========


class DocsURLsConfig(BaseModel):
    openapi: str
    redoc: str
    swagger: str


class DocsConfig(BaseModel):
    title: str
    description: str
    version: str
    urls: DocsURLsConfig


# ================================

# ======== DatabaseConfig ========


class DatabasePoolConfig(BaseModel):
    echo: bool
    size: int
    max_overflow: int


class DatabaseConfig(BaseModel):
    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str
    echo: bool
    pool: DatabasePoolConfig

    @property
    def dsn(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


# ================================

# ======== RedisConfig ========


class RedisConfig(BaseModel):
    username: str | None = None
    host: str
    port: int
    db: int
    password: str

    @property
    def dsn(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"


# ================================

# ======== AuthConfig ========


class SessionAccessConfig(BaseModel):
    secret_key: str
    algorithm: str
    issuer: str
    ttl_sec: int


class SessionRefreshConfig(BaseModel):
    hash_secret_key: str
    length: int
    ttl_sec: int


class SessionTokensConfig(BaseModel):
    access: SessionAccessConfig
    refresh: SessionRefreshConfig


class SessionConfig(BaseModel):
    tokens: SessionTokensConfig


class OTPConfig(BaseModel):
    storage_key_prefix: str
    hash_secret_key: str
    length: int
    ttl_min: int
    resend_cooldown_sec: int


class OTPTemplateConfig(BaseModel):
    subject: str
    body: str


class EmailTemplatesConfig(BaseModel):
    otp: OTPTemplateConfig


class EmailSMTPConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    from_name: str
    from_email: str
    timeout: int


class EmailConfig(BaseModel):
    smtp: EmailSMTPConfig
    templates: EmailTemplatesConfig


class AuthConfig(BaseModel):
    session: SessionConfig
    otp: OTPConfig
    email: EmailConfig


# ================================

# ======== CORSConfig ========


class CORSConfig(BaseModel):
    enabled: bool
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


# ================================


# ======== OpenRouterConfig ========


class OpenRouterConfig(BaseModel):
    api_key: str
    api_base_url: str


# ================================


# ======== AI Assistant Config ========


class AIAssistantConfig(BaseModel):
    model: str
    system_prompt: str
    confidence_score_threshold: float


# ================================

# ======== AppConfig ========


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=("config.yaml", "config.dev.yaml", "ai-assistant-config.yaml"),
        env_file=(".env", ".env.dev"),
        env_nested_delimiter="__",
        extra="ignore",
    )

    logging: LoggingConfig
    docs: DocsConfig
    database: DatabaseConfig
    redis: RedisConfig
    auth: AuthConfig
    cors: CORSConfig
    openrouter: OpenRouterConfig
    ai_assistant: AIAssistantConfig

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
            YamlConfigSettingsSource(settings_cls, deep_merge=True),
            env_settings,
            dotenv_settings,
            file_secret_settings,
            init_settings,
        )


# ================================
