from pydantic import (
    UUID7,
    BaseModel,
    Field,
)
from uuid6 import uuid7

from app.core.shared.enums import (
    DevicePlatformEnum,
    UserRoleEnum,
)

# device_id: DeviceIdVO
# device_platform: DevicePlatformEnum
# device_name: str | None = field(default=None)
# app_version: str

DEVICE_ID_EXAMPLE = uuid7()


class AuthenticatedUserInfoSchema(BaseModel):
    id: UUID7 = Field(
        ..., description="Unique identifier for the user.", examples=[DEVICE_ID_EXAMPLE]
    )
    role: UserRoleEnum = Field(
        ..., description="Role of the user.", examples=[UserRoleEnum.GUEST]
    )


class TokenInfoSchema(BaseModel):
    token: str = Field(
        ..., description="Token string.", examples=["eyJhbGciOiJIUzI1NiIsInR5c..."]
    )
    expires_in: int = Field(
        ..., description="Expiration time in seconds.", examples=[3600]
    )


class LoginAsGuestRequestSchema(BaseModel):
    device_id: UUID7 = Field(
        ...,
        description="Unique identifier for the device.",
        examples=[DEVICE_ID_EXAMPLE],
    )
    device_platform: DevicePlatformEnum = Field(
        ...,
        description="Platform of the device.",
        examples=[DevicePlatformEnum.ANDROID],
    )
    device_name: str | None = Field(
        None,
        description="Name of the device.",
        examples=["Pixel 9 Pro (Android 14)"],
    )
    app_version: str = Field(..., description="Version of the app.", examples=["1.0.0"])


class LoginAsGuestResponseSchema(BaseModel):
    access: TokenInfoSchema = Field(..., description="Access token information.")
    refresh: TokenInfoSchema = Field(..., description="Refresh token information.")
    user: AuthenticatedUserInfoSchema = Field(
        ..., description="Authenticated user information."
    )
