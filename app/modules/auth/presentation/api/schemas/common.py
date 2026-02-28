from pydantic import (
    BaseModel,
    Field,
)

from app.core.shared.enums import (
    DevicePlatformEnum,
)
from app.modules.users.presentation.api.schemas.common import (
    AuthenticatedUserInfoSchema,
)

DEVICE_ID_EXAMPLE = "019caaaa-0000-7000-a000-000000000001"
DEVICE_PLATFORM_EXAMPLE = DevicePlatformEnum.ANDROID
DEVICE_NAME_EXAMPLE = "Xiaomi 11T (Android 11)"
APP_VERSION_EXAMPLE = "1.0.0"

TOKEN_EXAMPLE = "itsshowinglikeitstheendoftheworld"
TOKEN_EXPIRES_IN_EXAMPLE = 3600


class TokenInfoSchema(BaseModel):
    token: str = Field(..., description="Token string.", examples=[TOKEN_EXAMPLE])
    expires_in: int = Field(
        ...,
        description="Expiration time in seconds.",
        examples=[TOKEN_EXPIRES_IN_EXAMPLE],
    )


class SuccessfulLoginSchema(BaseModel):
    access: TokenInfoSchema = Field(..., description="Access token information.")
    refresh: TokenInfoSchema = Field(..., description="Refresh token information.")
    user: AuthenticatedUserInfoSchema = Field(
        ..., description="Authenticated user information."
    )
