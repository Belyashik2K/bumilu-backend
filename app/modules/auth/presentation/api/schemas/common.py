from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.shared.enums import (
    DevicePlatformEnum,
    UserRoleEnum,
)

DEVICE_ID_EXAMPLE = "9af2a051-3c90-466b-98e7-a2da43f541b7"
DEVICE_PLATFORM_EXAMPLE = DevicePlatformEnum.ANDROID
DEVICE_NAME_EXAMPLE = "Xiaomi 11T (Android 11)"
APP_VERSION_EXAMPLE = "1.0.0"

EMAIL_EXAMPLE = "belyashik2k@dev.bumilu.ru"
VERIFICATION_CODE_EXAMPLE = "019840"

TOKEN_EXAMPLE = "itsshowinglikeitstheendoftheworld"


class AuthenticatedUserInfoSchema(BaseModel):
    id: UUID7 = Field(
        ..., description="Unique identifier for the user.", examples=[DEVICE_ID_EXAMPLE]
    )
    role: UserRoleEnum = Field(
        ..., description="Role of the user.", examples=[UserRoleEnum.GUEST]
    )


class TokenInfoSchema(BaseModel):
    token: str = Field(..., description="Token string.", examples=[TOKEN_EXAMPLE])
    expires_in: int = Field(
        ..., description="Expiration time in seconds.", examples=[3600]
    )


class SuccessfulLoginSchema(BaseModel):
    access: TokenInfoSchema = Field(..., description="Access token information.")
    refresh: TokenInfoSchema = Field(..., description="Refresh token information.")
    user: AuthenticatedUserInfoSchema = Field(
        ..., description="Authenticated user information."
    )
